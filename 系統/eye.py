from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer, Qt 
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import (QApplication, QMessageBox, )
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

import sys 
import clip
import sqlite3
import cv2 as cv
import mediapipe as mp
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates 
import math                                          
import Cover_ui as ui
import requests
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging
import json
from PIL import Image
import threading
import pandas as pd
import hashlib
from sklearn.impute import KNNImputer
import joblib
import re
import torch
from collections import deque
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import clip
import os
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import xgboost
import pickle as pkl

# 定義 CNN 模型結構（與保存時一致）
class EyeCNN(nn.Module):
    def __init__(self, input_channels=3):
        super(EyeCNN, self).__init__()
        self.conv1 = nn.Conv2d(input_channels, 16, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(2, 2)
        self.feature_dim = 64 * 28 * 28

    def forward(self, x):
        x = self.pool1(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2(x)))
        x = self.pool3(F.relu(self.conv3(x)))
        x = x.view(-1, self.feature_dim)
        return x

# 定義 CLIP + CNN + FCNN 模型結構（與保存時一致）
class CLIP_CNN_FCNN(nn.Module):
    def __init__(self, clip_feature_dim=512, cnn_feature_dim=64 * 28 * 28, num_classes=2):
        super(CLIP_CNN_FCNN, self).__init__()
        self.fc1 = nn.Linear(clip_feature_dim + cnn_feature_dim, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, num_classes)

    def forward(self, clip_features, cnn_features):
        combined = torch.cat((clip_features, cnn_features), dim=1)
        x = F.relu(self.fc1(combined))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class Window(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(Window,self).__init__()
        # 设置日志
        self.recent_results = deque(maxlen=10)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.processed_timestamps = set()  # 記錄已處理過的時間戳
        self.image_folder = os.path.join(current_dir, "photos/normal")
        #self.exhausted_folder = os.path.join(current_dir, "photos/exhausted")
        # 加載模型
        self.load_models()
        self.processing_images = False

        self.weighted_average = 25  # 默認 weighted_average 為 25 分鐘

        self.data_list = []
        self.record_state = 0  # 設置為休息狀態
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.2)
        self.mp_drawing = mp.solutions.drawing_utils

        self.token = ''
        self.init_time = time.time()
        self.setupUi(self)
        self.load_image_from_google_drive()
        self.nameBox.currentTextChanged.connect(lambda: self.user_list_onchange(1))   #page1 的choose user選單
        self.nameBox_2.currentTextChanged.connect(lambda: self.user_list_onchange(2)) #page2 開始後的choose user選單
        self.nameBox_3.currentTextChanged.connect(lambda: self.user_list_onchange(3)) #page3 Analysis的choose user選單
        self.nameBox_4.currentIndexChanged.connect(self.edit_onchange)                #page5 編輯頁面的choose user選單
         
        #self.distance_th.valueChanged.connect(self.update_threshold_values)   #距離的 UI 元素
        #self.bright_th.valueChanged.connect(self.update_threshold_values)     #亮度的 UI 元素
        #self.blink_th.valueChanged.connect(self.update_threshold_values)      #眨眼的 UI 元素
        #self.blink_num_th.valueChanged.connect(self.update_threshold_values)  #最低眨眼的UI 元素
        
        self.camera_active = False

        self.working_time.valueChanged.connect(self.working_time_onchange)   
        self.resting_time.valueChanged.connect(self.resting_time_onchange)

        self.start.clicked.connect(self.start_push_onchange)               #page1的Start按紐
        self.start.clicked.connect(self.update_threshold_values)  
        self.open_camera.clicked.connect(self.camera_onchange)             #page1的Camera按紐
        self.suggestion.clicked.connect(self.suggestion_push_onchange)     #page1的Suggestion按紐
        self.pushButton_sve.clicked.connect(self.save_numth_to_new_db)     #page2的Save按紐
        self.toolButton_finish.clicked.connect(self.finish_push_onchange)  #page2的Finish按紐
        self.send_to_line.clicked.connect(self.send_images_to_line)

        self.start.setEnabled(False)       # page1 禁用 Start 按鈕(尚未開啟相機)
        self.suggestion.setEnabled(False)  # page1 禁用 Suggestion 按鈕(尚未開啟相機) 
        self.login1_homebutton.setEnabled(True)
        self.introduction_send_pushButton.setEnabled(False)  # page7 禁用 送出 按鈕(等他按下已看完資訊才可以按)
        self.introduction_agree_radioButton.toggled.connect(self.toggle_send_button) #連接到開啟按鈕的
        self.introduction_send_pushButton.clicked.connect(self.submit_action)


        self.Savefile.clicked.connect(self.add_push_onchange)              #page4註冊的Save按紐      

            #page5編輯:顯示用戶歷史user_info
        self.nameBox_4.activated.connect(self.edit_onchange)               #page5編輯:更新用戶user_info
        self.Savefile_edit.clicked.connect(self.cover_data_to_new_db)      #page5編輯的Save按紐   
        self.deletefile_edit.clicked.connect(self.edit_delete_all)         #page5編輯的刪除按紐  
        self.Edit.clicked.connect(self.edit_clear)


        self.login.clicked.connect(lambda: self.switch_page(1))                 #page0首頁 按下Log in 跳轉至page1登入
        self.Analysis.clicked.connect(lambda: self.switch_page(3))              #page0首頁 按下Analysis 跳轉至page3查看日誌
        self.start.clicked.connect(lambda: self.switch_page(2))                 #page1 按下Start 跳轉至page2開始記錄
        self.toolButton_finish.clicked.connect(lambda: self.switch_page(6))     #page2 按下Finish 跳轉至page6填寫後測
        self.Edit.clicked.connect(lambda: self.switch_page(5))                  #page0 按下Edit 跳轉至page5編輯介面
        self.Signup.clicked.connect(lambda: self.switch_page(7))               #page0 按下Edit 跳轉至page4註冊介面
        self.login1_homebutton.clicked.connect(lambda: self.switch_page(0))     #page1 點選右上角返回首頁
        self.login2_homebutton.clicked.connect(lambda: self.switch_page(0))     #page2 點選右上角返回首頁
        self.login1_homebutton.clicked.connect(self.shut_onchange)              #page1 點選右上角返回首頁的同時關閉系統
        self.login2_homebutton.clicked.connect(self.shut_onchange)              #page2 點選右上角返回首頁的同時關閉系統
        self.analysis_homebutton.clicked.connect(lambda: self.switch_page(0))   #page3 點選右上角返回首頁
        self.signup_homebutton.clicked.connect(lambda: self.switch_page(0))     #page4 點選右上角返回首頁
        self.edit1_homebutton.clicked.connect(lambda: self.switch_page(0))      #page5 點選右上角返回首頁
        self.introduction_send_pushButton.clicked.connect(lambda: self.switch_page(4))   #page7 按下送出 跳轉至page4註冊介面

        #timer
        self.timer_camera = QTimer() #初始化定時器
        self.timer_warm = QTimer() #初始化定時器
        self.timer_camera.timeout.connect(self.update_progress_value)  
        self.timer_warm.timeout.connect(self.check_status)
        self.work_time = self.working_time.value()                         #page1獲取UI框框中的數值(work_time)
        self.rest_time = self.resting_time.value()                         #page1獲取UI框框中的數值(rest_time)
        self.blink_thres = self.blink_th.value()                           #page1獲取UI框框中的數值(blink_thres)
        self.bright_thres = self.bright_th.value()                         #page1獲取UI框框中的數值(bright_thres)
        self.distance_thres = self.distance_th.value()                     #page1獲取UI框框中的數值(distance_thres)
        self.blink_threshold_per_minute_value = self.blink_num_th.value()  #page1獲取UI框框中的數值(blink_threshold_per_minute_value)
        self.blink_thres_2 = self.blink_th_2.value()                           #page2獲取UI框框中的數值(blink_thres_2)
        self.bright_thres_2 = self.bright_th_2.value()                         #page2獲取UI框框中的數值(bright_thres_2)
        self.distance_thres_2 = self.distance_th_2.value()                     #page2獲取UI框框中的數值(distance_thres_2)
        self.blink_threshold_per_minute_value_2 = self.blink_num_th_2.value()  #page2獲取UI框框中的數值(blink_threshold_per_minute_value_2)

        self.exercise_type.addItem('None')
        self.exercise_type.addItem('close eye')
        self.exercise_type.addItem('jumping jack')

        self.blink_per_minute = 0 
        self.is_exhausted = False  
        self.exhausted_work_counter = 0
        self.too_close_count = 0 


        # 初始化並監聽值的變化
        self.blink_th.valueChanged.connect(lambda: self.update_threshold(self.blink_th, self.blink_th_2))
        self.bright_th.valueChanged.connect(lambda: self.update_threshold(self.bright_th, self.bright_th_2))
        self.distance_th.valueChanged.connect(lambda: self.update_threshold(self.distance_th, self.distance_th_2))
        self.blink_num_th.valueChanged.connect(lambda: self.update_threshold(self.blink_num_th, self.blink_num_th_2))
        #self.blink_num_th_2.valueChanged.connect(lambda: self.update_threshold(self.blink_num_th_2, self.blink_num_th))

        self.last_exhausted_time_str = None  # 初始化上次按下的時間


        # 初始化疲勞狀態
        self.Exhausted_state = 0
        self.Exhausted_count = 0
        self.next_threshold = 15
        # 連接按鈕點擊事件
        self.pushButton_Exhausted.clicked.connect(self.pushButton_Exhausted_onchange)
        self.last_time_recorded = None  # 用來記錄上次的時間
        # 獲取 pushButton_Exhausted 和 listView 控件
        self.pushButton_Exhausted = self.findChild(QtWidgets.QPushButton, 'pushButton_Exhausted')
        self.listView = self.findChild(QtWidgets.QListView, 'listView')

        # 使用 QStandardItemModel 來管理 ListView 中的數據
        self.listView_model = QtGui.QStandardItemModel(self.listView)
        self.listView.setModel(self.listView_model)
        # variables 
        self.FONT_SIZE = 1
        # calendar
        #self.select_range.addItem('Every Minute')
        self.calendarWidget.selectionChanged.connect(self.calendar)

        self.frame_counter =0
        self.CEF_COUNTER =0
        self.total_blink =0
        self.eye_area= 800
        self.ratio = 0
        self.count = 0
        self.brightness_value = 0
        # constants
        self.eye_close_frame =1
        self.previous_time = 200
        self.area_record = np.ones(self.previous_time)
        self.FONTS =cv.FONT_HERSHEY_COMPLEX
        self.EYE_STATE = 0
        self.ratio_thres = 4.5
        self.eye_area_thres_high = 1500
        self.eye_area_thres_low = 200
        self.eye_area_record = 800
        self.eye_area_ratio = 0.7
        # face bounder indices 
        self.FACE_OVAL=[ 10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103,67, 109]
        self.FACE_OVAL_SIM = [156,383,397]
        # lips indices for Landmarks
        self.LIPS=[ 61, 146, 91, 181, 84, 17, 314, 405, 321, 375,291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95,185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78 ]
        self.LOWER_LIPS =[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
        self.UPPER_LIPS=[ 185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78] 
        # Left eyes indices 
        self.LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
        self.LEFT_EYEBROW =[ 336, 296, 334, 293, 300, 276, 283, 282, 295, 285 ]
        # right eyes indices
        self.RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  
        self.RIGHT_EYEBROW=[ 70, 63, 105, 66, 107, 55, 65, 52, 53, 46 ]
        # Center
        self.CENTER_POINT = [9,8,168]
        self.BODY = [22,20,18,16,14,12,24,23,11,13,15,17,19,21]
        self.HEAD = [8,6,5,4,0,1,2,3,7]
        self.map_face_mesh = mp.solutions.face_mesh
        self.status = 'run' # start # end
        self.blink_counter = 0
        self.area_counter = 0
        self.bright_counter = 0
        self.frame_counter = 0
        self.passing_time = 0

        #store minute information
        self.count_minute = 0 
        self.previous_minute = 0
        self.count_bright = 0
        self.count_blink = 0
        self.count_distance = 0

        #record time
        self.previous_time_step = 0
        self.now_time_step = 0
        self.pass_time = 0 
        self.time_status = 'start'
        

        #jump
        self.previous_state = -1
        self.count_hand = 0
        self.count_jump = 0
        self.shoulder_pos = []
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.current_user  = str(self.nameBox_2.currentText())

        # 取得當前程式碼檔案的目錄
        if getattr(sys, 'frozen', False):  # 判斷是否為打包後的執行檔
            current_dir = os.path.dirname(sys.executable)  # 執行檔所在目錄
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))

        # 連接主資料庫
        self.db_path = os.path.join(current_dir, 'database.db')
        #print(f"資料庫路徑1：{self.db_path}")


        self.con = sqlite3.connect(self.db_path)
        self.cursorObj = self.con.cursor()

        self.start_time_for_database = 0

        # 創建 `None` 和 `threshold` 表格
        self.cursorObj.execute(f'''
            CREATE TABLE IF NOT EXISTS None_data(
                year INTEGER, 
                month INTEGER, 
                day INTEGER, 
                hour INTEGER, 
                minute INTEGER, 
                distance REAL, 
                brightness INTEGER, 
                blink INTEGER, 
                state INTEGER, 
                Exhausted_state INTEGER,
                start_time_for_database TEXT 
            );
        ''')
        self.cursorObj.execute('''
            CREATE TABLE IF NOT EXISTS threshold(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user TEXT, 
                line_token TEXT, 
                distance_area REAL, 
                distance_ratio REAL, 
                brightness INTEGER, 
                blink INTEGER,
                blink_num INTEGER,
                insert_time TEXT
            );
        ''')
        # 檢查是否已經有初始數據
        self.cursorObj.execute('SELECT COUNT(*) FROM threshold WHERE user = ?', ('None',))
        count = self.cursorObj.fetchone()[0]

        # 如果記錄不存在，則插入初始數據
        if count == 0:
            self.cursorObj.execute('''
                INSERT INTO threshold(
                    user, line_token, distance_area, distance_ratio, brightness, blink, blink_num
                ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                ('None', '', self.eye_area_record, self.eye_area_ratio, 60, 4, 15)
            )
            self.con.commit()
        # 讀取 threshold 表數據並更新界面
        cursor = self.cursorObj.execute("SELECT * FROM threshold").fetchall()
        existing_users = set()  # 用於儲存已加入過的使用者名稱

        for row in cursor:
            user_name = str(row[1]) 
            
            # 檢查名稱是否已存在於 existing_users 集合中
            if user_name not in existing_users:
                # 如果名稱不存在，則新增到下拉選單
                self.nameBox.addItem(user_name)
                self.nameBox_2.addItem(user_name)
                self.nameBox_3.addItem(user_name)
                self.nameBox_4.addItem(user_name)
                
                # 將名稱加入集合中以追蹤已新增的名稱
                existing_users.add(user_name)
            else:
                #print(f"{user_name} 已存在，跳過新增")
                pass


        #建立 user_info 表格
        self.con = sqlite3.connect(self.db_path)
        self.cursorObj = self.con.cursor()
        self.cursorObj.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                username TEXT,
                birthday TEXT,
                gender TEXT,
                right_eye_condition TEXT,
                right_eye_degree TEXT,
                right_eye_shine TEXT,
                right_eye_shine_degree REAL,
                left_eye_condition TEXT,
                left_eye_degree REAL,
                left_eye_shine TEXT,
                left_eye_shine_degree REAL,
                eye_situation_value1 INTEGER,
                eye_situation_value2 INTEGER,
                eye_situation_value3 INTEGER,
                eye_situation_value4 INTEGER,
                eye_situation_value5 INTEGER,
                use_situation1 TEXT,
                use_situation2 TEXT,
                use_situation3 TEXT,
                use_situation_value4 INTEGER,
                use_situation_value5 TEXT,
                habit1 TEXT,
                habit2 TEXT,
                habit3 TEXT,
                habit4 TEXT,
                habit5 TEXT,
                habit6 TEXT,
                habit7 TEXT,
                line_token TEXT,
                start_time_for_database TEXT
            );
        ''')

        # 創建 posttest 表格
        self.cursorObj.execute('''
            CREATE TABLE IF NOT EXISTS None_posttest (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_1 TEXT,
                question_2 TEXT,
                question_3 TEXT,
                question_4 TEXT,
                question_5 TEXT,
                question_6 TEXT,        
                question_7 INTEGER,
                question_8 INTEGER,
                question_9 INTEGER,
                question_10 INTEGER,
                question_11 INTEGER,
                question_12 TEXT,
                submission_time TEXT,  -- 填表的時間
                start_time_for_database TEXT  -- 按下start的時間
            );
        ''')
        self.con.commit()
# 創建 user_id 表格(關聯式資料庫)
        self.cursorObj.execute('''
            CREATE TABLE IF NOT EXISTS user_id (
                user_name TEXT,
                test_id TEXT --start_time_for_database
            );
        ''')
        self.con.commit()

        # 設置按鈕點擊事件
        self.Sendout_Button.clicked.connect(self.sendout)
        self.Savefile.clicked.connect(self.Save)

        print("Save button connected to posttest and user_info")
    # 在初始化過程中設置 weighted_average
    def load_models(self):
        """
        加載 CLIP 和 CLIP_CNN_FCNN 模型
        """
        print("模型加載中...")

        # 加載 CLIP 模型
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
        self.model_clip, self.preprocess_fn = clip.load("ViT-B/32", device=self.device)
        self.model_clip.eval()
        # 初始化 CNN 模型（不需外部權重）
        self.cnn_model = EyeCNN().to(self.device)
        self.cnn_model.eval()
        print("EyeCNN 模型加載成功")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        combined_model_path = os.path.join(current_dir, 'CNN_model.pth')
        try:
            self.model_cnn = torch.load(combined_model_path, map_location=self.device)           
            self.model_cnn.eval()
            print("CLIP_CNN_FCNN 模型加載成功")
        except Exception as e:
            print(f"CLIP_CNN_FCNN 模型加載失敗: {e}")
            raise


 
    def extract_features(self, image_paths):
        """
        提取批次圖片的 CLIP 特徵和 CNN 特徵
        """
        clip_features_list = []
        cnn_features_list = []
        try:
            for image_path in image_paths:
                print(f"🔍 開始處理圖片: {image_path}")

                # 加載圖片並轉換為張量
                img = Image.open(image_path).convert("RGB")
                image_tensor = self.preprocess_fn(img).unsqueeze(0).to(self.device)

                # 提取 CLIP 特徵
                with torch.no_grad():
                    clip_features = self.model_clip.encode_image(image_tensor).float()
                    clip_features_list.append(clip_features)

                # 提取 CNN 特徵
                with torch.no_grad():
                    cnn_features = self.cnn_model(image_tensor)
                    cnn_features_list.append(cnn_features)

            # 合併特徵
            combined_clip_features = torch.cat(clip_features_list, dim=0)
            combined_cnn_features = torch.cat(cnn_features_list, dim=0)
            return combined_clip_features, combined_cnn_features

        except Exception as e:
            print(f"特徵提取失敗: {e}")
            return None, None


    def predict_fatigue(self, image_paths):
        """
        預測批次圖片的疲勞狀態
        """
        try:
            # 提取 CLIP 和 CNN 特徵
            clip_features, cnn_features = self.extract_features(image_paths)

            # 檢查特徵是否有效
            if clip_features is None or cnn_features is None:
                print("特徵提取失敗，無法進行預測")
                return None

            # 模型推理
            with torch.no_grad():
                output = self.model_cnn(clip_features, cnn_features)
                predictions = torch.argmax(output, dim=1).cpu().numpy()  # 返回批次分類結果
                return predictions

        except Exception as e:
            print(f"預測失敗: {e}")
            return None


    def check_and_process_images(self):
        """
        檢查是否有新圖片並即時處理
        """
        print("⚙️ 圖片處理進行中...")

        # 獲取當前時間
        current_time = datetime.now()

        # 檢查是否有新圖片
        image_files = [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) if f.lower().endswith('.jpg')]
        if not image_files:
            print("❗等待新圖片生成...")
            return

        # 秒級分組
        second_grouped_images = {}
        for file in image_files:
            try:
                timestamp_str = re.search(r"(\d{8}-\d{6}-\d{3})", file).group(1)
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S-%f")
                second_str = timestamp.strftime("%Y%m%d-%H%M%S")

                if second_str not in second_grouped_images:
                    second_grouped_images[second_str] = []
                second_grouped_images[second_str].append(file)
            except AttributeError:
                print(f"❗ 無法處理圖片文件: {file}")

        print(f"✅ 秒級分組完成，共找到 {len(second_grouped_images)} 個秒級時間戳組")

        # 處理每個秒級時間戳的圖片
        for second_str, files in second_grouped_images.items():
            print(f"📸 開始處理時間戳: {second_str}, 總共 {len(files)} 張圖片")

            # 執行分類
            predictions = self.predict_fatigue(files)
            if predictions is None:
                print("❗ 批次分類失敗，無有效結果")
                continue

            # 記錄分類結果
            for idx, pred in enumerate(predictions):
                result_text = "疲勞" if pred == 1 else "正常"
                print(f"圖片 {files[idx]} 的分類結果：{result_text}")

            # 刪除已處理的圖片
            for file in files:
                try:
                    os.remove(file)
                    print(f"🗑️ 已刪除圖片: {os.path.basename(file)}")
                except FileNotFoundError:
                    print(f"⚠️ 無法刪除圖片，可能已被處理: {os.path.basename(file)}")



    # 圖片時間戳分組
    def group_images_by_minute(self, image_files):
        grouped_images = {}
        for file in image_files:
            try:
                timestamp_str = re.search(r"(\d{8}-\d{6})", file).group(1)
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
                minute_str = timestamp.strftime("%Y%m%d-%H%M")

                if minute_str not in grouped_images:
                    grouped_images[minute_str] = []
                grouped_images[minute_str].append(file)
            except AttributeError:
                print(f"❗ 無法處理圖片文件: {file}")

        print(f"✅ 圖片分組完成，共找到 {len(grouped_images)} 個時間戳組")
        return grouped_images    # 主處理函式


    def process_images(self):
        """非阻塞方式的圖片處理"""
        self.recent_results = deque(maxlen=10)  # 儲存最近 10 分鐘結果
        self.processed_timestamps = set()  # 記錄已處理過的時間戳（精確到秒）
        self.last_processed_minute = None  # 紀錄上次處理的分鐘
        self.timer = QTimer()  # 初始化計時器
        self.timer.timeout.connect(self.check_and_process_images)  # 綁定定時器執行檢查
        self.timer.start(1000)  # 每 1 秒執行一次檢查
        print("圖片處理已啟動")
        self.check_and_process_images()  # 立即執行一次，避免首次延遲

    def check_and_process_images111(self):
        """檢查是否有新圖片並即時處理"""
        print("⚙️ 圖片處理進行中...")

        # 獲取當前時間
        current_time = datetime.now()

        # 檢查是否有新圖片
        image_files = [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) if f.lower().endswith('.jpg')]

        #image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith('.jpg')]
        if not image_files:
            print("❗等待新圖片生成...")
            return
        predictions = []
        for image_file in image_files:
        # 確保 image_file 是字符串
            if isinstance(image_file, list):
                print(f"❗ 無效的圖片路徑: {image_file}, 跳過")
                continue

            prediction = self.predict_fatigue(image_file)
            if prediction is not None:
                predictions.append(prediction)

        if not predictions:
            print("❗ 批次分類失敗，無有效結果")
            return

        for idx, pred in enumerate(predictions):
            result_text = "疲勞" if pred == 1 else "正常"
            print(f"圖片 {image_files[idx]} 的分類結果：{result_text}")
        # 秒級分組
        second_grouped_images = {}
        for file in image_files:
            try:
                timestamp_str = re.search(r"(\d{8}-\d{6}-\d{3})", file).group(1)
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S-%f")
                second_str = timestamp.strftime("%Y%m%d-%H%M%S")

                if second_str not in second_grouped_images:
                    second_grouped_images[second_str] = []
                second_grouped_images[second_str].append(file)
            except AttributeError:
                print(f"❗ 無法處理圖片文件: {file}")

        print(f"✅ 秒級分組完成，共找到 {len(second_grouped_images)} 個秒級時間戳組")

        # 處理每個秒級時間戳的圖片
        minute_results = []
        for second_str, files in second_grouped_images.items():
            print(f"📸 開始處理時間戳: {second_str}, 總共 {len(files)} 張圖片")
            total_predictions = []

            # 每批次處理 10 張圖片
            for i in range(0, len(files), 10):
                batch_files = [os.path.join(self.image_folder, f) for f in sorted(files)[i:i+10]]
                print(f"🔄 批次處理圖片 {i + 1} 至 {i + len(batch_files)}")

                # 執行分類
                predictions = self.predict_fatigue(batch_files)
                print(f"📊 批次分類結果: {predictions}")

                # 記錄每張圖片分類結果
                for idx, pred in enumerate(predictions, start=i + 1):
                    state = "疲勞" if pred == 1 else "正常"
                    print(f"圖片 {idx}: {state}")

                # 更新結果到 total_predictions
                total_predictions.extend(predictions)

                # 刪除已處理的圖片
                for file in batch_files:
                    try:
                        os.remove(file)
                        print(f"🗑️ 已刪除圖片: {os.path.basename(file)}")
                    except FileNotFoundError:
                        print(f"⚠️ 無法刪除圖片，可能已被處理: {os.path.basename(file)}")

            # 更新秒級結果
            fatigue_count = sum(total_predictions)
            fatigue_state = 1 if fatigue_count > 0 else 0
            minute_results.append(fatigue_state)

        # 分鐘級判斷
        current_minute = current_time.strftime("%Y%m%d-%H%M")
        if current_minute != self.last_processed_minute:
            self.last_processed_minute = current_minute
            minute_fatigue_state = 1 if sum(minute_results) > 0.6 * len(minute_results) else 0
            self.recent_results.append(minute_fatigue_state)
            print(f"✅ 分鐘級結果: 疲勞比例: {sum(minute_results)}/{len(minute_results)}, 判斷: {'疲勞 (狀態 1)' if minute_fatigue_state else '正常 (狀態 0)'}")

            # 打印最近結果
            print(f"📊 最近 10 分鐘結果: {list(self.recent_results)}")

            # 疲勞狀態通知
            if len(self.recent_results) >= 3 and list(self.recent_results)[-3:] == [1, 1, 1]:
                print("⚠️ 連續 3 分鐘偵測到疲勞狀態")
            if len(self.recent_results) == 10 and list(self.recent_results) == [1] * 10:
                print("⚠️ 連續 10 分鐘偵測到疲勞狀態，請立即休息！")


            # 標記為已處理
            self.processed_timestamps.add(timestamp)
    def initialize_working_time(self):
        """
        初始化工作時間和 weighted_average。
        """
        try:
            # 預設工作時間為 25 分鐘
            self.work_time = self.working_time.value() or 25
            self.weighted_average = 25  # 默認 weighted_average 為 25 分鐘
            # 如果有預測結果，更新 weighted_average
            if hasattr(self, 'predicted_weighted_average') and self.predicted_weighted_average > 0:
                self.weighted_average = self.predicted_weighted_average

            # 如果 weighted_average > 25，更新 UI 的工作時間
            if self.weighted_average > self.work_time:
                self.working_time.setValue(self.weighted_average)  # 更新 UI 框框
                self.work_time = self.weighted_average
                print(f"初始化：weighted_average 為 {self.weighted_average} 分鐘，更新工作時間。")
            else:
                print(f"初始化：weighted_average 為 {self.weighted_average} 分鐘，保持默認工作時間。")

        except Exception as e:
            print(f"初始化 weighted_average 時發生錯誤：{e}")

    def predict_user_fatigue(self):
        """
        根據當前用戶的處理數據和模型進行疲勞時間預測，並輸出結果。
        """
        logging.basicConfig(
            filename="fatigue_prediction.log",
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        print("開始執行疲勞預測函數")

        def convert_to_time_format(minutes):
            """將分鐘數轉換為 HH:MM:SS 格式"""
            total_seconds = int(minutes * 60)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02}:{minutes:02}:{seconds:02}"

        try:
            # 動態生成文件路徑
            current_user = self.current_user
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(current_dir, f"{current_user}_final_data.csv")
            selected_features_file = os.path.join(current_dir, 'selected_features.pkl')

            # 檢查數據文件是否存在
            if not os.path.exists(data_file):
                logging.error(f"用戶 {current_user} 的數據文件不存在，跳過預測。")
                return

            # 模型和特徵文件路徑
            model_path = os.path.join(current_dir, 'xgb_model.pkl')
            model2_path = os.path.join(current_dir, 'rnn_model.h5')

            # 加載數據與模型
            filtered_data = pd.read_csv(data_file)
            regressor = load(model_path)  # 加載 XGBoost 模型
            regressor2 = load_model(model2_path)  # 加載 RNN 模型 (.h5)
            feature = load(selected_features_file)  # 加載特徵列表

            # 提取特徵與標籤
            X_new = filtered_data[feature]
            y_new = filtered_data['time_diff_to_first_exhausted']

            print(f"Filtered data shape: {filtered_data.shape}")
            print(f"Selected features: {feature}")

            # === 即時標準化每個欄位 ===
            scaler = MinMaxScaler()
            X_new_scaled = scaler.fit_transform(X_new)  # 即時標準化選定的特徵

            # 預測
            y_pred_xgb = regressor.predict(X_new_scaled)
            X_rnn = np.expand_dims(X_new_scaled, axis=1)  # 增加時間步維度
            rnn_predictions = regressor2.predict(X_rnn).flatten()  # 預測並展平結果
            y_pred_ensemble = 0.89 * y_pred_xgb + 0.11 * rnn_predictions

            # 計算加權平均
            weighted_average = np.mean(y_pred_ensemble)
            final_time = convert_to_time_format(weighted_average)

            # 更新結果到變量和 UI
            self.predicted_weighted_average = weighted_average
            self.weighted_average = weighted_average
            self.working_time.setValue(int(weighted_average))

            # 顯示結果
            msg = QMessageBox()
            msg.setWindowTitle("Fatigue Prediction Result")
            msg.setText(
                f"<p>預估 {final_time} 開始感到眼睛疲勞</p>"
                f"<p>約 {weighted_average:.0f} 分鐘後</p>"
            )
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            print("彈出視窗完成")

        except Exception as e:
            logging.error(f"預測過程失敗：{e}")
            QMessageBox.critical(
                self,
                "預測錯誤",
                f"發生錯誤: {e}",
                QMessageBox.Ok,
            )

    def load_image_from_google_drive(self):
        # Google Drive 圖片的 URL
        firstpage_url = "https://drive.google.com/uc?id=1Y_709FXJCueCi3QbS5-um3-dCBn5vc3i"
        background_url = "https://drive.google.com/uc?id=1Fb0NNLVGbzou0y8B1bgVlxBHgQp9LByz"
        homeicon_url = "https://drive.google.com/uc?id=1M4OYrou7PXCGU2oAXEPcPfi8tDnNtAoL"

        # 定義圖片的下載路徑
        firstpage_download_path = os.path.expanduser('~/Pictures/firstpage.png')
        background_download_path = os.path.expanduser('~/Pictures/background.png')
        homeicon_download_path = os.path.expanduser('~/Pictures/homeicon.png')

        # 檢查目錄是否存在，如果不存在則創建目錄
        os.makedirs(os.path.dirname(firstpage_download_path), exist_ok=True)

        # 定義圖片的 URL 和路徑對應字典
        images = {
            firstpage_url: firstpage_download_path,
            background_url: background_download_path,
            homeicon_url: homeicon_download_path
        }

        # 下載並保存圖片的函數
        def download_image(url, path):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(path, 'wb') as file:
                        file.write(response.content)
                    #print(f"圖片已下載並保存在 {path}")
                else:
                    print(f"無法下載圖片：{url}")
            except Exception as e:
                print(f"下載圖片時出現錯誤：{e}")

        # 檢查並下載圖片
        for url, path in images.items():
            if not os.path.exists(path):
                download_image(url, path)
            #else:
                #print(f"圖片已存在，從本地加載: {path}")
                

        # 加載並顯示圖片到對應的 UI 標籤
        self.load_image_from_path(firstpage_download_path, self.firstpage_picture_label)
        for label in [self.secondpage_picture_label_2, self.secondpage_picture_label_3,
                    self.secondpage_picture_label_4, self.secondpage_picture_label_5,
                    self.secondpage_picture_label_6, self.secondpage_picture_label_7,
                    self.secondpage_picture_label_8]:
            self.load_image_from_path(background_download_path, label)

        # 加載 home icon 並設置到按鈕
        self.load_home_icon(homeicon_download_path)


    def load_image_from_path(self, image_path, label):
        # 加載本地圖片並顯示
        if os.path.exists(image_path):
            image = QtGui.QImage(image_path)
            if not image.isNull():
                pixmap = QtGui.QPixmap(image)
                label.setPixmap(pixmap.scaled(1108, 670, QtCore.Qt.IgnoreAspectRatio))
                label.setAlignment(QtCore.Qt.AlignCenter)
            else:
                print(f"Failed to load image from {image_path}")
        else:
            print(f"File does not exist: {image_path}")

    def load_home_icon(self, icon_path):
        # 加載本地 home icon 圖示
        if os.path.exists(icon_path):
            homeicon_image = QtGui.QImage(icon_path)
            if not homeicon_image.isNull():
                homeicon_pixmap = QtGui.QPixmap(homeicon_image)
                homeicon_icon = QtGui.QIcon(homeicon_pixmap)  # 將 QPixmap 轉換為 QIcon
                self.login1_homebutton.setIcon(homeicon_icon)  # 設置 QIcon 為按鈕的圖標
                self.login1_homebutton.setIconSize(QtCore.QSize(30, 30))  # 設置圖標大小
                self.login2_homebutton.setIcon(homeicon_icon)  # 設置 QIcon 為按鈕的圖標
                self.login2_homebutton.setIconSize(QtCore.QSize(30, 30))  # 設置圖標大小
                self.analysis_homebutton.setIcon(homeicon_icon)  # 設置 QIcon 為按鈕的圖標
                self.analysis_homebutton.setIconSize(QtCore.QSize(30, 30))  # 設置圖標大小
                self.signup_homebutton.setIcon(homeicon_icon)  # 設置 QIcon 為按鈕的圖標
                self.signup_homebutton.setIconSize(QtCore.QSize(30, 30))  # 設置圖標大小
                self.edit1_homebutton.setIcon(homeicon_icon)  # 設置 QIcon 為按鈕的圖標
                self.edit1_homebutton.setIconSize(QtCore.QSize(30, 30))  # 設置圖標大小
            else:
                print(f"Failed to create QPixmap from {icon_path}")
        else:
            print(f"Icon file does not exist: {icon_path}")

    def create_user_data(self):
        #self.current_user  = str(self.nameBox_2.currentText())
        print(f"create_user_data中current user {self.current_user}")
        # 連接主資料庫
        self.con = sqlite3.connect(self.db_path)
        self.cursorObj = self.con.cursor()
        self.start_time_for_database = 0

        # 創建  `threshold` 表格
        self.cursorObj.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.current_user}_data(
                year INTEGER, 
                month INTEGER, 
                day INTEGER, 
                hour INTEGER, 
                minute INTEGER, 
                distance REAL, 
                brightness INTEGER, 
                blink INTEGER, 
                state INTEGER, 
                Exhausted_state INTEGER,
                start_time_for_database TEXT 
            );
        ''')
    
    def shut_onchange(self):
        self.status = 'shutting_down'

    # 註冊頁面存檔功能
    def save_data_to_new_db(self):   # 註冊頁面存檔功能
        try:
            # Collect data from the UI
            name = self.name_input.text()
            username = self.user_name_input.text()
            birthday = self.birthday_input.text()
            line_token = self.line_token_input.text()
            gender = '男生' if self.sex_man_button.isChecked() else '女生'

    # Set right eye condition and degree based on myopia (negative) or hyperopia (positive)
            right_eye_condition = '近視' if self.right_eye_in_button.isChecked() else '遠視'
            right_eye_degree = self.right_eye_degree_input.text()
            if right_eye_degree:
                right_eye_degree = -abs(float(right_eye_degree)) if right_eye_condition == '近視' else abs(float(right_eye_degree))
            right_eye_shine = '有' if self.right_eye_shine_button.isChecked() else '無'
            right_eye_shine_degree = self.right_eye_shine_input.text()

    # Set left eye condition and degree similarly
            left_eye_condition = '近視' if self.left_eye_in_button.isChecked() else '遠視'
            left_eye_degree = self.left_eye_degree_input.text()
            if left_eye_degree:
                left_eye_degree = -abs(float(left_eye_degree)) if left_eye_condition == '近視' else abs(float(left_eye_degree))            
            left_eye_shine = '有' if self.left_eye_shine_button.isChecked() else '無'
            left_eye_shine_degree = self.left_eye_shine_input.text()

            eye_situation_value1 = self.eye_situation_button_group1.id(self.eye_situation_button_group1.checkedButton()) if self.eye_situation_button_group1.checkedButton() else None
            eye_situation_value2 = self.eye_situation_button_group2.id(self.eye_situation_button_group2.checkedButton()) if self.eye_situation_button_group2.checkedButton() else None
            eye_situation_value3 = self.eye_situation_button_group3.id(self.eye_situation_button_group3.checkedButton()) if self.eye_situation_button_group3.checkedButton() else None
            eye_situation_value4 = self.eye_situation_button_group4.id(self.eye_situation_button_group4.checkedButton()) if self.eye_situation_button_group4.checkedButton() else None
            eye_situation_value5 = self.eye_situation_button_group5.id(self.eye_situation_button_group5.checkedButton()) if self.eye_situation_button_group5.checkedButton() else None

            use_situation1 = '是' if self.use_situation_yes_button1.isChecked() else '否'
            use_situation2 = self.use_situation2_combobox.currentText()
            use_situation3 = '是' if self.use_situation_yes_button3.isChecked() else '否'
            use_situation_value4 = self.use_situation4_combobox.currentText()
            use_situation_value5 = self.use_situation5_combobox.currentText()

            habit1 = '是' if self.habit_yes_button1.isChecked() else '否'
            habit2 = self.habit_combobox2.currentText()
            habit3 = self.habit_combobox3.currentText()
            habit4 = self.habit_combobox4.currentText()
            habit5 = self.habit_combobox5.currentText()
            habit6 = self.habit_combobox6.currentText()

            habit7 = []
            if self.habit_close_checkbox7.isChecked():
                habit7.append('閉目養神')
            if self.habit_exercise_checkbox7.isChecked():
                habit7.append('眼部運動')
            if self.habit_other_checkbox7.isChecked():
                habit7.append('其他')
            habit7_str = ', '.join(habit7)
            # Validation: Check if required fields are filled
            if not (name and username and birthday):
                QMessageBox.warning(self, "錯誤", "請填寫完整")
                return

            # Check if the username already exists in the database
            self.cursorObj.execute('SELECT * FROM user_info WHERE username = ?', (username,))
            username_result = self.cursorObj.fetchone()

            if username_result:
                # If a matching username is found, notify the user that the username already exists
                QMessageBox.information(self, "提示", f"使用者 '{username}' 已經存在，無法新增重複使用者。")
                return  # Exit the function without saving    

            # Now save the new data
            self.cursorObj.execute('''
                INSERT INTO user_info (
                    name, username, birthday, gender, 
                    right_eye_condition, right_eye_degree, right_eye_shine, right_eye_shine_degree,
                    left_eye_condition, left_eye_degree, left_eye_shine, left_eye_shine_degree,
                    eye_situation_value1, eye_situation_value2, eye_situation_value3, eye_situation_value4, eye_situation_value5,
                    use_situation1, use_situation2, use_situation3, use_situation_value4, use_situation_value5,
                    habit1, habit2, habit3, habit4, habit5, habit6, habit7, line_token
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                name, username, birthday, gender, 
                right_eye_condition, right_eye_degree, right_eye_shine, right_eye_shine_degree,
                left_eye_condition, left_eye_degree, left_eye_shine, left_eye_shine_degree,
                eye_situation_value1, eye_situation_value2, eye_situation_value3, eye_situation_value4, eye_situation_value5,
                use_situation1, use_situation2, use_situation3, use_situation_value4, use_situation_value5,
                habit1, habit2, habit3, habit4, habit5, habit6, habit7_str, line_token
            ))

            # Commit the new data
            self.con.commit()

            # Show success message and switch page
            success_msg = QMessageBox()
            success_msg.setText("資料已存檔")
            success_msg.setIcon(QMessageBox.Information)
            success_msg.setWindowTitle("成功")
            success_msg.buttonClicked.connect(lambda: self.switch_page(0))  # Switch to page_0 after clicking "OK"
            success_msg.exec()

            # 5. Reset fields after successful submission
            # Clear text input fields
            self.name_input.clear()
            self.user_name_input.clear()
            self.birthday_input.clear()
            self.line_token_input.clear()
            self.right_eye_degree_input.clear()
            self.right_eye_shine_input.clear()
            self.left_eye_degree_input.clear()
            self.left_eye_shine_input.clear()

            # Uncheck radio buttons
            self.sex_group.setExclusive(False)  # 暫時關閉互斥
            self.sex_man_button.setChecked(False)
            self.sex_women_button.setChecked(False)
            self.sex_group.setExclusive(True)   # 恢復互斥功能
 
            #右眼狀況
            self.right_eye_group.setExclusive(False)
            self.right_eye_out_button.setChecked(False)
            self.right_eye_in_button.setChecked(False)
            self.right_eye_group.setExclusive(True)

            #右眼散光
            self.right_eye_shine_group.setExclusive(False)
            self.right_eye_shine_button.setChecked(False)
            self.right_eye_shine_group.setExclusive(True)
            
            #左眼狀況
            self.left_eye_group.setExclusive(False)
            self.left_eye_out_button.setChecked(False)
            self.left_eye_in_button.setChecked(False)
            self.left_eye_group.setExclusive(True)
            
            #左眼散光
            self.left_eye_shine_group.setExclusive(False)
            self.left_eye_shine_button.setChecked(False)
            self.left_eye_shine_group.setExclusive(True)

            # 暫時取消互斥性
            self.eye_situation_button_group1.setExclusive(False)
            self.eye_situation_button_group2.setExclusive(False)
            self.eye_situation_button_group3.setExclusive(False)
            self.eye_situation_button_group4.setExclusive(False)
            self.eye_situation_button_group5.setExclusive(False)
            
            # 清除選中狀態
            for button in self.eye_situation_button_group1.buttons():
                button.setChecked(False)
            for button in self.eye_situation_button_group2.buttons():
                button.setChecked(False)
            for button in self.eye_situation_button_group3.buttons():
                button.setChecked(False)
            for button in self.eye_situation_button_group4.buttons():
                button.setChecked(False)
            for button in self.eye_situation_button_group5.buttons():
                button.setChecked(False)
            
            # 恢復互斥性
            self.eye_situation_button_group1.setExclusive(True)
            self.eye_situation_button_group2.setExclusive(True)
            self.eye_situation_button_group3.setExclusive(True)
            self.eye_situation_button_group4.setExclusive(True)
            self.eye_situation_button_group5.setExclusive(True)
            
            #長時間使用電子產品
            self.use_situation1_group.setExclusive(False)
            self.use_situation_yes_button1.setChecked(False)
            self.use_situation_no_button1.setChecked(False)
            self.use_situation1_group.setExclusive(True)

            #長時間使用電子產品
            self.use_situation3_group.setExclusive(False)
            self.use_situation_yes_button3.setChecked(False)
            self.use_situation_no_button3.setChecked(False)
            self.use_situation3_group.setExclusive(True)

            #長時間使用電子產品
            self.habit1_group.setExclusive(False)
            self.habit_no_button1.setChecked(False)
            self.habit_yes_button1.setChecked(False)
            self.habit1_group.setExclusive(True)

            # 休息方式
            self.habit_close_checkbox7.setChecked(False)
            self.habit_exercise_checkbox7.setChecked(False)
            self.habit_other_checkbox7.setChecked(False)

            #所有下拉式選單
            self.use_situation2_combobox.setCurrentIndex(0)
            self.use_situation4_combobox.setCurrentIndex(0)
            self.use_situation5_combobox.setCurrentIndex(0)
            self.habit_combobox2.setCurrentIndex(0)
            self.habit_combobox3.setCurrentIndex(0)
            self.habit_combobox4.setCurrentIndex(0)
            self.habit_combobox5.setCurrentIndex(0)
            self.habit_combobox6.setCurrentIndex(0)

        except Exception as e:
            # Show error message in case of failure
            QMessageBox.warning(self, "錯誤", f"存檔失敗: {str(e)}")



    def update_threshold(self, source, target):
        # 更新 target 的值為 source 的值
        target.setValue(source.value())
    
    #插入&更換目前用戶
    def check_and_add_user(self):
        # 獲取使用者輸入的 user_name
        user_name = self.user_name_input.text()

        # 如果 user_name 輸入框不為空
        if user_name:
            try:
                # 檢查該 user_name 是否已經存在於 threshold 表中
                query = "SELECT COUNT(*) FROM threshold WHERE user = ?"
                self.cursorObj.execute(query, (user_name,))
                result = self.cursorObj.fetchone()

                # 如果使用者不存在於資料庫中，則新增該使用者
                if result[0] == 0:
                    # 新增該使用者到 threshold 表
                    self.cursorObj.execute("INSERT INTO threshold (user) VALUES (?)", (user_name,))
                    self.con.commit()
                    print(f"New user {user_name} added to the database.")
                else:
                    print(f"User {user_name} already exists in the database.")

                # 將該 user_name 設為 current_user
                self.current_user = user_name
                print(f"Current user set to {self.current_user}")

            except sqlite3.Error as e:
                print(f"Database error: {e}")

        else:
            print("User name input is empty, no action taken.")

    #插入/更新用戶Line金鑰
    def update_line_token_in_db(self):
        # 獲取使用者在 line_token_input 中輸入的值
        line_token = self.line_token_input.text()

        # 使用 self.current_user 作為資料庫更新的依據
        user_name = self.current_user  # 這應該是選中的使用者名稱

        # 檢查 line_token 是否有值，並且確保已選擇使用者名稱
        if line_token and user_name:
            try:
                # 更新資料庫中的 line_token 欄位，根據選擇的 user_name
                query = "UPDATE threshold SET line_token = ? WHERE user = ?"
                self.cursorObj.execute(query, (line_token, user_name))

                # 如果沒有該使用者的資料，則插入新的記錄
                if self.cursorObj.rowcount == 0:
                    self.cursorObj.execute(
                        "INSERT INTO threshold (user, line_token) VALUES (?, ?)",
                        (user_name, line_token)
                    )

                # 提交變更
                self.con.commit()
                print(f"Line token for user {user_name} updated successfully.")

            except sqlite3.Error as e:
                print(f"Database error: {e}")

        else:
            print("Line token is empty or no user selected, no update performed.")

    #按下註冊頁面的Save鍵
    def Save(self):
        self.check_and_add_user()
        self.update_line_token_in_db()
        self.save_data_to_new_db()

    #換頁功能      
    def switch_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
        if index == 6:  # 當進入 page_6 編輯頁面時
            self.load_user_names_into_edit_dropdown()


    def load_user_names_into_edit_dropdown(self):
        # 獲取使用者輸入的名稱
        text = str(self.user_name_input.text())

        # 檢查名稱是否為空
        if text == '':
            print('名稱為空，無法新增')
            return  # 名稱為空，直接返回

        # 檢查名稱是否已經存在於 nameBox 中
        for i in range(self.nameBox.count()):
            if self.nameBox.itemText(i) == text:
                print(f'名稱 "{text}" 已經存在於 nameBox 中，無法新增')
                return  # 名稱已存在於下拉選單，直接返回

        # 檢查名稱是否已經存在於資料庫中
        query = "SELECT COUNT(*) FROM threshold WHERE user = ?"
        self.cursorObj.execute(query, (text,))
        result = self.cursorObj.fetchone()

        if result[0] > 0:
            print(f"名稱 '{text}' 已經存在於資料庫中，無法新增")
            return  # 名稱已存在於資料庫，直接返回

        # 名稱有效且未重複，新增到下拉選單和資料庫
        self.nameBox.addItem(text)
        self.nameBox_2.addItem(text)
        self.nameBox_3.addItem(text)
        self.nameBox_4.addItem(text)

        # 插入新使用者到資料庫
        self.cursorObj.execute(
            "INSERT INTO threshold (user, line_token, distance_area, distance_ratio, brightness, blink, blink_num) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (text, self.line_token_input.text(), self.eye_area_record, self.eye_area_ratio, 60, 4, 15)
        )
        self.con.commit()
        print(f"新用戶 {text} 已加入資料庫")

        
        if (text != ''):
            self.con = sqlite3.connect(self.db_path)
            self.cursorObj = self.con.cursor()

            try:
                print(f"Creating table for user: {self.current_user}")

                self.cursorObj.execute(f'''CREATE TABLE IF NOT EXISTS {self.current_user}_data (
                    year INTEGER, 
                    month INTEGER, 
                    day INTEGER, 
                    hour INTEGER, 
                    minute INTEGER, 
                    distance REAL, 
                    brightness INTEGER, 
                    blink INTEGER, 
                    state INTEGER, 
                    Exhausted_state INTEGER, 
                    start_time_for_database TEXT
                )''')                
                self.cursorObj.execute(f'''
                    CREATE TABLE IF NOT EXISTS {self.current_user}_posttest (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question_1 TEXT,
                        question_2 TEXT,
                        question_3 TEXT,
                        question_4 TEXT,
                        question_5 TEXT,
                        question_6 TEXT,        
                        question_7 INTEGER,
                        question_8 INTEGER,
                        question_9 INTEGER,
                        question_10 INTEGER,
                        question_11 INTEGER,
                        question_12 TEXT,
                        submission_time TEXT,  -- 填表的時間
                        start_time_for_database TEXT -- 按下start的時間
                    );
                ''')

                self.cursorObj.execute("insert or ignore into threshold(user,line_token,  distance_area, distance_ratio, brightness, blink, blink_num) VALUES (?,?,?,?,?,?,?)" ,(text,self.line_token_input.text(),self.eye_area_record,self.eye_area_ratio,60,4,15))
                self.con.commit()
            except:
                self.showMainWindow('Not valid name!')
        else:
            print('empty')


    def lineNotifyMessage(self,msg):
        try:
            headers = {
                "Authorization": "Bearer " + self.token, 
                "Content-Type" : "application/x-www-form-urlencoded"
            }
            
            payload = {'message': msg}
            r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        except:
            pass

    def summary_report(self):
        # 取得今天的日期
        year = datetime.today().strftime("%Y")
        month = datetime.today().strftime("%m")
        day = datetime.today().strftime("%d")
        today_date = datetime.today().strftime("%Y-%m-%d")
        self.cursorObj = self.con.cursor()
        self.current_user  = str(self.nameBox_2.currentText())

        # 檢查當前使用者的表是否存在，避免操作不存在的表
        table_name = f"{self.current_user}_data"
        self.cursorObj.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        table_exists = self.cursorObj.fetchone()

        if not table_exists:
            print(f"資料表 {table_name} 不存在，無法生成報告。")
            return  # 若資料表不存在，則結束函數

        # 查詢當天所有的記錄
        cursor = self.cursorObj.execute(
            f"SELECT year, month, day, hour, minute, distance, brightness, blink, state, Exhausted_state "
            f"FROM {self.current_user}_data WHERE year=? AND month=? AND day=? ORDER BY hour, minute",
            (year, month, day)
        )

        records = cursor.fetchall()

        # 記錄開始時間
        start_time = self.init_time
        start_hour = int(datetime.fromtimestamp(start_time).strftime("%H"))
        start_minute = int(datetime.fromtimestamp(start_time).strftime("%M"))

        # 用於當次和當日的變量
        total_dis, total_bri, total_blink = [], [], []
        dis_session, bri_session, blink_session = [], [], []
        use_time_total, rest_time_total = 0, 0
        use_time_session, rest_time_session = 0, 0
        exercise_types = []  # 記錄當次的運動方式
        in_session = False
        current_exercise = None

        # 迭代當天的所有記錄
        for i in records:
            current_time = datetime(int(i[0]), int(i[1]), int(i[2]), int(i[3]), int(i[4]))
            state = i[8]  # 狀態
            distance = float(i[5])
            brightness = int(i[6])
            blink = int(i[7])

            # 計算當日使用狀況
            if state == 2:  # 工作狀態
                use_time_total += 1
                total_dis.append(distance)
                total_bri.append(brightness)
                total_blink.append(blink)
            
            # 開始計算當次使用情形
            if (i[3] > start_hour or (i[3] == start_hour and i[4] >= start_minute)) and state == 2:
                # 如果當前時間是工作狀態且在開始時間之後，記錄當次使用情形
                use_time_session += 1
                dis_session.append(distance)
                bri_session.append(brightness)
                blink_session.append(blink)
                in_session = True
            elif in_session and state == 0:
                # 記錄休息狀態並加入運動方式
                rest_time_session += 1
                if current_exercise:
                    exercise_types.append(current_exercise)

            # 記錄當前休息時選擇的運動方式
            if state == 0:
                rest_time_total += 1
                current_exercise = self.exercise_type.currentText()  # 記錄當前運動類型
            else:
                current_exercise = None

        # 定義亮度描述函數
        def get_brightness_description(avg_brightness):
            if avg_brightness < 100:
                return "過暗"
            elif 100 <= avg_brightness < 120:
                return "普通"
            elif 120 <= avg_brightness <= 200:
                return "充足"
            else:
                return "過亮"

        # 計算當次使用平均值
        avg_dis_session = round(sum(dis_session) / len(dis_session), 2) if dis_session else 0.00
        avg_bri_session = round(sum(bri_session) / len(bri_session), 2) if bri_session else 0.00
        avg_blink_session = round(sum(blink_session) / len(blink_session), 2) if blink_session else 0.00
        brightness_description_session = get_brightness_description(avg_bri_session)

        # 計算當日使用平均值
        avg_dis_total = round(sum(total_dis) / len(total_dis), 2) if total_dis else 0.00
        avg_bri_total = round(sum(total_bri) / len(total_bri), 2) if total_bri else 0.00
        avg_blink_total = round(sum(total_blink) / use_time_total, 2) if use_time_total > 0 else 0.00
        brightness_description_total = get_brightness_description(avg_bri_total)

        # 獲取所有不同的運動類型
        exercise_types_report = ', '.join(set(exercise_types)) if exercise_types else '無'

        # 組裝報告訊息
        message = (
            f"【EyesMyself】 {today_date}\n"
            f"--- 當次使用情形 ---\n"
            f"使用時間: {use_time_session} 分鐘\n"
            f"休息時間: {rest_time_session} 分鐘\n"
            f"平均距離: {avg_dis_session}\n"
            f"光源情況: {brightness_description_session}（平均亮度: {avg_bri_session}）\n"
            f"平均眨眼次數: {avg_blink_session}\n"
            f"休息方式: {exercise_types_report}\n"
            f"距離過近提醒次數: {self.too_close_count}\n"
            f"--- 今日使用情形 ---\n"
            f"使用時間: {use_time_total} 分鐘\n"
            f"休息時間: {rest_time_total} 分鐘\n"
            f"平均距離: {avg_dis_total}\n"
            f"整體光源情況: {brightness_description_total}（平均亮度: {avg_bri_total}）\n"
            f"平均眨眼次數: {avg_blink_total}\n"
        )

        # 發送LINE通知
        self.lineNotifyMessage(message)

        # 打印到控制台
        print(message)
    
    def want_line_onchange(self):
        # Check if the line_token_input has a value to enable LINE notifications automatically
        if self.line_token_input.text():  # If the line_token_input has a value
            self.line_token_input.setEnabled(True)  # Enable the line_token field
            self.line_token_input.setText(self.line_token_input.text())  # Set the line token text
            print("LINE notifications enabled for user:", self.current_user)
            # Optionally send a notification that LINE is set up
            #self.lineNotifyMessage("Notification setup complete for this user.")
        else:
            # If no line_token is found, disable the line_token input field
            self.line_token_input.setEnabled(False)
            self.line_token_input.clear()  # Clear the line token field if no token is found
            print("LINE notifications disabled (no token found) for user:", self.current_user)

    #新增blink per minute            
    def update_blink_threshold(self, value):
        self.blink_threshold_per_minute_value  = value
    def update_blink_threshold_1(self, value):
        self.blink_threshold_per_minute_value_1 = value  # 更新 self.blink_threshold_per_minute_value_1

    def update_threshold_values(self):   # page1 開始前調整閾值
        # 從 UI 欄位中獲取更新的閾值
        distance_ratio = self.distance_th.value()
        brightness = self.bright_th.value()
        blink = self.blink_th.value()
        blink_num = self.blink_num_th.value()
        # 從下拉選單中獲取當前使用者
        current_user = self.current_user

        # 獲取當前時間並格式化
        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # 查詢 user_info 表中的 line_token
            self.cursorObj.execute("SELECT line_token FROM user_info WHERE username = ? ORDER BY id DESC LIMIT 1", (current_user,))
            result = self.cursorObj.fetchone()
            if result:
                line_token = result[0]
            else:
                line_token = ""  # 如果找不到則設為空值
            
            # 插入新的閾值紀錄至資料庫，包含當前時間
            insert_query = """
            INSERT INTO threshold (user,line_token,distance_area, distance_ratio, brightness, blink, blink_num, insert_time)
            VALUES (?, ?, ?, ?, ?, ?,?,?)
            """
            self.cursorObj.execute(insert_query, (current_user,line_token,self.eye_area_record,distance_ratio, brightness, blink, blink_num, insert_time))
            #self.token=line_token

            # 提交更改（不關閉連線）
            self.con.commit()
            print(f"New threshold values inserted for user {current_user} at {insert_time}")
            
            # 成功插入後的訊息視窗
            '''msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("資料插入成功")
            msg.setText("已成功插入一筆新的閾值資料！")
            msg.setInformativeText(
                f"使用者: {current_user}\n"
                f"插入時間: {insert_time}\n"
                f"距離閾值: {distance_ratio}\n"
                f"亮度閾值: {brightness}\n"
                f"眨眼閾值: {blink}\n"
                f"每分鐘最低眨眼數: {blink_num}"
            )
            msg.exec_()'''
        
        except sqlite3.Error as e:
            print(f"Error inserting new threshold data: {e}")
            # 錯誤訊息視窗
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("資料插入失敗")
            error_msg.setText("插入閾值資料時發生錯誤")
            error_msg.setInformativeText(str(e))
            error_msg.exec_()

    def save_numth_to_new_db(self):  # page2 開始後更新閾值功能
        # 取得 UI 中的閾值與選取的使用者名稱
        distance_record = self.distance_th_2.value()
        brightness_record = self.bright_th_2.value()
        blink_record = self.blink_th_2.value()
        blink_per_minute_record = self.blink_num_th_2.value()
        user = self.nameBox_2.currentText()
        

        # 獲取當前時間並格式化
        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # 查詢 user_info 表中的 line_token
            self.cursorObj.execute("SELECT line_token FROM user_info WHERE username = ? ORDER BY id DESC LIMIT 1", (user,))
            result = self.cursorObj.fetchone()
            if result:
                line_token = result[0]
            else:
                line_token = ""  # 如果找不到則設為空值

            # 插入新的閾值紀錄至資料庫，包含當前時間
            insert_query = """
            INSERT INTO threshold (user, line_token, distance_area, distance_ratio, brightness, blink, blink_num, insert_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursorObj.execute(
                insert_query, 
                (user,line_token, self.eye_area_record, distance_record, brightness_record, blink_record, blink_per_minute_record, insert_time)
            )
            
            # 獲取剛插入的資料的 id
            last_id = self.cursorObj.lastrowid
            #self.token=line_token

            # 提交更改（不關閉連線）
            self.con.commit()
            print(f"New threshold values inserted for user {user} at {insert_time} with ID {last_id}")
            
            # 成功插入後的訊息視窗
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("資料插入成功")
            msg.setText("資料更新成功！")
            '''msg.setInformativeText(
                f"使用者: {user}\n"
                f"插入時間: {insert_time}\n"
                f"距離閾值: {distance_record}\n"
                f"亮度閾值: {brightness_record}\n"
                f"眨眼閾值: {blink_record}\n"
                f"每分鐘最低眨眼數: {blink_per_minute_record}\n"
                f"資料 ID: {last_id}"
            )'''
            msg.exec_()
            
        except sqlite3.Error as e:
            print(f"Error inserting new threshold data: {e}")
            # 錯誤訊息視窗
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("資料插入失敗")
            error_msg.setText("插入閾值資料時發生錯誤")
            error_msg.setInformativeText(str(e))
            error_msg.exec_()

    def change_index(self,value):
        self.stackedWidget.setCurrentIndex(value)
    def user_list_onchange(self, user=1): 
        try:
            # 獲取選定的用戶名稱
            if user == 1:
                new_user = str(self.nameBox.currentText())
            elif user == 2:
                new_user = str(self.nameBox_2.currentText())
            elif user == 3:
                new_user = str(self.nameBox_3.currentText())
            else:
                new_user = None

            # 檢查新用戶是否有效
            if not new_user or new_user == "None":
                print(f"無效的用戶選擇。保持原有的 current_user: {self.current_user}")
                return  # 保留 current_user 原值，不更新

            # 更新 current_user 為新用戶
            old_user = self.current_user
            self.current_user = new_user
            print(f"更新 current_user：由 {old_user} 改為 {self.current_user}")

            # 重置與新用戶相關的變量
            self.predicted_weighted_average = None  # 清空預測的加權平均時間
            self.weighted_average = 25  # 默認 25 分鐘
            self.working_time.setValue(25)  # 更新 UI 中的工作時間為默認值

            # 檢查是否有數據文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(current_dir, f"{self.current_user}_final_data.csv")
            if not os.path.exists(data_file):
                print(f"用戶 {self.current_user} 的數據文件不存在，無法進行預測，保持當前用戶並允許數據更新。")
                # 跳過預測但保留 current_user 值
                self.weighted_average = 0
                pass

            # 暫停信號，避免重複觸發
            self.nameBox.blockSignals(True)
            self.nameBox_2.blockSignals(True)
            self.nameBox_3.blockSignals(True)

            # 同步所有 nameBox 顯示選定的 current_user
            self.nameBox.setCurrentText(self.current_user)
            self.nameBox_2.setCurrentText(self.current_user)
            self.nameBox_3.setCurrentText(self.current_user)
            print(f"暫停信號後同步所有namebox的current_user: {self.current_user}")
            # 恢復信號
            self.nameBox.blockSignals(False)
            self.nameBox_2.blockSignals(False)
            self.nameBox_3.blockSignals(False)

            # 查詢資料庫並更新 UI
            self.query_user_data()

            # 若頁面是 page1 或 page2，執行模型推理
            if user == 1 or user == 2:
                print("執行疲勞時間推理...")
                self.predict_user_fatigue()
            else:
                print("進入分析頁面，執行額外分析功能...")

        except Exception as e:
            print(f"使用者切換時發生錯誤：{e}")
        finally:
            print("user_list_onchange 函數執行完畢。")
            print(f"current_user : {self.current_user}")
    def query_user_data(self):
        """查詢使用者數據並更新 UI"""
        try:
            # 檢查使用者是否有效
            if not self.current_user or self.current_user == "None":
                print("當前使用者無效，無法查詢數據。")
                return

            with sqlite3.connect(self.db_path) as con:
                cursor = con.cursor()
                query = """
                SELECT line_token, distance_ratio, brightness, blink, blink_num
                FROM threshold
                WHERE user = ? 
                ORDER BY ROWID DESC 
                LIMIT 1
                """
                cursor.execute(query, (self.current_user,))
                result = cursor.fetchone()

                if result:
                    line_token, distance_ratio, brightness, blink, blink_num = result
                    print(f"查詢到的最後插入數據，對應使用者: {self.current_user}")
                    print(f"資料內容: {result}")

                    # 更新 UI
                    self.distance_th.setValue(float(distance_ratio))
                    self.bright_th.setValue(int(brightness))
                    self.blink_th.setValue(float(blink))
                    self.blink_num_th.setValue(int(blink_num))
                    self.token = line_token
                else:
                    print(f"查無資料，對應使用者: {self.current_user}，資料表: threshold")

        except sqlite3.Error as db_error:
            print(f"資料庫操作時發生錯誤：{db_error}")
        except Exception as e:
            print(f"查詢數據時發生未知錯誤：{e}")
    def edit_onchange(self):  #編輯使用者介面 : 顯示用戶歷史資料
        selected_index = self.nameBox_4.currentIndex()# 獲取選擇的用戶索引
        if selected_index > 0:
            # 根據索引獲取選擇的用戶名稱
            selected_user = self.nameBox_4.currentText()  
            # 查詢資料庫，使用選中的用戶名
            self.cursorObj.execute('SELECT * FROM user_info WHERE username = ? AND id = (SELECT MAX(id) FROM user_info WHERE username = ?)', (selected_user, selected_user))
            user_data = self.cursorObj.fetchone()
            if user_data:
                print(f"Raw data: {user_data[29]}")
                self.name_input_edit.setText(user_data[1])  # 顯示姓名
                
                self.birthday_input_edit.setText(user_data[3])
                
                gender = user_data[4]  # 取出性別欄位值
                if gender == "男生":
                    self.sex_man_button_edit.setChecked(True)
                elif gender == "女生":
                    self.sex_women_button_edit.setChecked(True)
                    
                right_eye_condition = user_data[5]  
                if right_eye_condition == "近視":
                    self.right_eye_in_button_edit.setChecked(True)
                elif right_eye_condition == "遠視":
                    self.right_eye_out_button_edit.setChecked(True)
                    
                self.right_eye_degree_input_edit.setText(user_data[6])
                
                right_eye_shine_condition = user_data[7]  
                if right_eye_shine_condition == "閃光":
                    self.right_eye_shine_button_edit.setChecked(True)
                    
                #self.right_eye_shine_input_edit.setText(f"{user_data[8]:.1f}")  # 保留一位小數
                self.right_eye_shine_input_edit.setText(str(user_data[8]))
                
                
                left_eye_condition = user_data[9]  
                if left_eye_condition == "近視":
                    self.left_eye_in_button_edit.setChecked(True)
                elif left_eye_condition == "遠視":
                    self.left_eye_out_button_edit.setChecked(True)
                    
                #self.left_eye_degree_input_edit.setText(f"{user_data[10]:.1f}")  # 保留一位小數
                self.left_eye_degree_input_edit.setText(str(user_data[10]))
                
                left_eye_shine_condition = user_data[11]  
                if left_eye_shine_condition == "閃光":
                    self.left_eye_shine_button_edit.setChecked(True)
                    
                #self.left_eye_shine_input_edit.setText(f"{user_data[12]:.1f}")  # 保留一位小數
                self.left_eye_shine_input_edit.setText(str(user_data[12]))

                if user_data:
                    # 設置單選按鈕的選中狀態
                    eye_situation_value1 = user_data[13]  # 這是從資料庫中讀取到的數值
                    print(f"eye_situation_value1 from database: {eye_situation_value1}")
                    if eye_situation_value1:
                        button_to_select = self.eye_situation_button_group1_edit.button(int(eye_situation_value1))
                        if button_to_select:
                            button_to_select.setChecked(True)
                            self.update()

                        print(f"Button {button_to_select.objectName()} is now checked: {button_to_select.isChecked()}")

                    eye_situation_value2 = user_data[14]
                    if eye_situation_value2:
                        button_to_select = self.eye_situation_button_group2_edit.button(int(eye_situation_value2))
                        if button_to_select:
                            button_to_select.setChecked(True)
                            self.update()
                        print(f"Button {button_to_select.objectName()} is now checked: {button_to_select.isChecked()}")

                    eye_situation_value3 = user_data[15]
                    if eye_situation_value3:
                        button_to_select = self.eye_situation_button_group3_edit.button(int(eye_situation_value3))
                        if button_to_select:
                            button_to_select.setChecked(True)
                            self.update()

                    eye_situation_value4 = user_data[16]
                    if eye_situation_value4:
                        button_to_select = self.eye_situation_button_group4_edit.button(int(eye_situation_value4))
                        if button_to_select:
                            button_to_select.setChecked(True)
                            self.update()

                    eye_situation_value5 = user_data[17]
                    if eye_situation_value5:
                        button_to_select = self.eye_situation_button_group5_edit.button(int(eye_situation_value5))
                        if button_to_select:
                            button_to_select.setChecked(True)
                            self.update()                    
              
                use_situation1 = user_data[18]  
                if use_situation1 == "是":
                    self.use_situation_yes_button1_edit.setChecked(True)
                elif use_situation1 == "否":
                    self.use_situation_no_button1_edit.setChecked(True)
                    
                use_situation2 = user_data[19]
                # 設定當前選項
                if use_situation2 in ["3小時以內", "3至6小時", "6至9小時", "9至12小時", "12小時以上"]:
                    self.use_situation2_combobox_edit.setCurrentText(use_situation2)  # 設定為當前選項
                else:
                    self.use_situation2_combobox_edit.setCurrentText("3小時以內")  # 或其他預設值
                
                use_situation3 = user_data[20]  
                if use_situation3 == "是":
                    self.use_situation_yes_button3_edit.setChecked(True)
                elif use_situation3 == "否":
                    self.use_situation_no_button3_edit.setChecked(True)
                
                use_situation_value4 = user_data[21]
                # 設定當前選項
                if use_situation_value4 in ["電腦自動調整", "不常調整", "每次使用都會調整"]:
                    self.use_situation4_combobox_edit.setCurrentText(use_situation_value4)  # 設定為當前選項
                else:
                    self.use_situation4_combobox_edit.setCurrentText("電腦自動調整")  # 或其他預設值

                use_situation_value5 = user_data[22]  
                # 設定當前選項
                if use_situation_value5 in ["室內共用燈光", "室內專屬燈光", "室外自然光", "以上皆無"]:
                    self.use_situation5_combobox_edit.setCurrentText(use_situation_value5)  # 設定為當前選項
                else:
                    self.use_situation5_combobox_edit.setCurrentText("室內共用燈光")  # 或其他預設值    
                
                habit1 = user_data[23]  
                if habit1 == "是":
                    self.habit_yes_button1_edit.setChecked(True)
                elif habit1 == "否":
                    self.habit_no_button1_edit.setChecked(True)
                
                habit2 = user_data[24]
                # 設定當前選項
                if habit2 in ["無", "半年一次", "一年一次", "更頻繁"]:
                    self.habit_combobox2_edit.setCurrentText(habit2)  # 設定為當前選項
                else:
                    self.habit_combobox2_edit.setCurrentText("無")  # 或其他預設值
                    
                habit3 = user_data[25]
                if habit3 in ["低於4小時", "4至6小時", "6至8小時", "高於8小時"]:
                    self.habit_combobox3_edit.setCurrentText(habit3)  # 設定為當前選項
                else:
                    self.habit_combobox3_edit.setCurrentText("低於4小時")  # 或其他預設值
                    
                habit4 = user_data[26]
                # 設定當前選項
                if habit4 in ["0或1次", "2或3次", "4或5次", "6次以上"]:
                    self.habit_combobox4_edit.setCurrentText(habit4)  # 設定為當前選項
                else:
                    self.habit_combobox4_edit.setCurrentText("0或1次")  # 或其他預設值
                    
                habit5 = user_data[27]
                # 設定當前選項
                if habit5 in ["無休息", "1小時內", "1至2小時", "2至3小時", "3至4小時", "4至5小時", "5小時以上"]:
                    self.habit_combobox5_edit.setCurrentText(habit5)  # 設定為當前選項
                else:
                    self.habit_combobox5_edit.setCurrentText("無休息")  # 或其他預設值
                    
                habit6 = user_data[28]
                # 設定當前選項
                if habit6 in ["10分鐘內", "11至30分鐘", "31至60分鐘", "60分鐘以上"]:
                    self.habit_combobox6_edit.setCurrentText(habit6)  # 設定為當前選項
                else:
                    self.habit_combobox6_edit.setCurrentText("10分鐘內")  # 或其他預設值

                # 假設 user_data[8] 是包含所有 checkbox 狀態的欄位，格式為 "1,0,1"
                checkbox_data = user_data[29].split(',')  
                print(f"Raw data: {user_data[29]}")
                # 讀取資料時，去除項目前後的空白
                checkbox_data = [item.strip() for item in user_data[29].split(',')]
                if len(checkbox_data) >= 3:  # 確保有三個狀態值
                    # 設置 habit_close_checkbox7_edit 的狀態
                    if checkbox_data[0] == "閉目養神":
                        self.habit_close_checkbox7_edit.setChecked(True)
                    else:
                        self.habit_close_checkbox7_edit.setChecked(False)

                    # 設置 habit_exercise_checkbox7_edit 的狀態
                    if checkbox_data[1] == "眼部運動":
                        self.habit_exercise_checkbox7_edit.setChecked(True)
                    else:
                        self.habit_exercise_checkbox7_edit.setChecked(False)

                    # 設置 habit_other_checkbox7_edit 的狀態
                    if checkbox_data[2] == "其他":
                        self.habit_other_checkbox7_edit.setChecked(True)
                    else:
                        self.habit_other_checkbox7_edit.setChecked(False)
                
                self.line_token_input_edit.setText(user_data[30])
                
            else:
                print("沒有找到該用戶的資料")
        
     
                
        input_fields = [
            self.name_input_edit,
            self.birthday_input_edit,
            self.line_token_input_edit,
            self.right_eye_degree_input_edit,
            self.left_eye_degree_input_edit,
            self.habit_combobox2_edit,
            self.habit_combobox3_edit,
            self.habit_combobox4_edit,
            self.habit_combobox5_edit,
            self.habit_combobox6_edit,]

        buttons = [
            self.sex_man_button_edit,
            self.sex_women_button_edit,
            self.right_eye_out_button_edit,
            self.right_eye_in_button_edit,
            self.right_eye_shine_button_edit,
            self.left_eye_out_button_edit,
            self.left_eye_in_button_edit,
            self.left_eye_shine_button_edit,
            self.use_situation_yes_button1_edit,
            self.use_situation_no_button1_edit,
            self.use_situation_yes_button3_edit,
            self.use_situation_no_button3_edit,
            self.habit_yes_button1_edit,
            self.habit_no_button1_edit,]
        
        all_buttons = self.temp_button1_edit + self.temp_button2_edit + self.temp_button3_edit + self.temp_button4_edit + self.temp_button5_edit +self.temp_button2_edit

        checkboxes = [
            self.habit_close_checkbox7_edit,
            self.habit_other_checkbox7_edit,
            self.habit_exercise_checkbox7_edit,]

        comboboxes = [
            self.use_situation2_combobox_edit,]

        # 打開所有控件
        for field in input_fields + buttons + checkboxes + comboboxes + all_buttons:
            field.setEnabled(True)
        self.Savefile_edit.setEnabled(True)
        self.deletefile_edit.setEnabled(True)  
                    
    def edit_clear(self): #清空編輯介面
        # 5. Reset fields after successful submission
        # Clear text input fields
        self.name_input_edit.clear()
        self.birthday_input_edit.clear()
        self.line_token_input_edit.clear()
        self.right_eye_degree_input_edit.clear()
        self.right_eye_shine_input_edit.clear()
        self.left_eye_degree_input_edit.clear()
        self.left_eye_shine_input_edit.clear()

        # Uncheck radio buttons
        self.sex_group_edit.setExclusive(False)  # 暫時關閉互斥
        self.sex_man_button_edit.setChecked(False)
        self.sex_women_button_edit.setChecked(False)
        self.sex_group_edit.setExclusive(True)   # 恢復互斥功能
 
        #右眼狀況
        self.right_eye_group_edit.setExclusive(False)
        self.right_eye_out_button_edit.setChecked(False)
        self.right_eye_in_button_edit.setChecked(False)
        self.right_eye_group_edit.setExclusive(True)

        #右眼散光
        self.right_eye_shine_group_edit.setExclusive(False)
        self.right_eye_shine_button_edit.setChecked(False)
        self.right_eye_shine_group_edit.setExclusive(True)
            
        #左眼狀況
        self.left_eye_group_edit.setExclusive(False)
        self.left_eye_out_button_edit.setChecked(False)
        self.left_eye_in_button_edit.setChecked(False)
        self.left_eye_group_edit.setExclusive(True)
            
        #左眼散光
        self.left_eye_shine_group_edit.setExclusive(False)
        self.left_eye_shine_button_edit.setChecked(False)
        self.left_eye_shine_group_edit.setExclusive(True)

        # 暫時取消互斥性
        self.eye_situation_button_group1_edit.setExclusive(False)
        self.eye_situation_button_group2_edit.setExclusive(False)
        self.eye_situation_button_group3_edit.setExclusive(False)
        self.eye_situation_button_group4_edit.setExclusive(False)
        self.eye_situation_button_group5_edit.setExclusive(False)
        
        # 清除選中狀態
        for button in self.eye_situation_button_group1_edit.buttons():
            button.setChecked(False)
        for button in self.eye_situation_button_group2_edit.buttons():
            button.setChecked(False)
        for button in self.eye_situation_button_group3_edit.buttons():
            button.setChecked(False)
        for button in self.eye_situation_button_group4_edit.buttons():
            button.setChecked(False)
        for button in self.eye_situation_button_group5_edit.buttons():
            button.setChecked(False)
        
        # 恢復互斥性
        self.eye_situation_button_group1_edit.setExclusive(True)
        self.eye_situation_button_group2_edit.setExclusive(True)
        self.eye_situation_button_group3_edit.setExclusive(True)
        self.eye_situation_button_group4_edit.setExclusive(True)
        self.eye_situation_button_group5_edit.setExclusive(True)
            
        #長時間使用電子產品
        self.use_situation1_group_edit.setExclusive(False)
        self.use_situation_yes_button1_edit.setChecked(False)
        self.use_situation_no_button1_edit.setChecked(False)
        self.use_situation1_group_edit.setExclusive(True)

        #長時間使用電子產品
        self.use_situation3_group_edit.setExclusive(False)
        self.use_situation_yes_button3_edit.setChecked(False)
        self.use_situation_no_button3_edit.setChecked(False)
        self.use_situation3_group_edit.setExclusive(True)

        #長時間使用電子產品
        self.habit1_group_edit.setExclusive(False)
        self.habit_no_button1_edit.setChecked(False)
        self.habit_yes_button1_edit.setChecked(False)
        self.habit1_group_edit.setExclusive(True)

        # 休息方式
        self.habit_close_checkbox7_edit.setChecked(False)
        self.habit_exercise_checkbox7_edit.setChecked(False)
        self.habit_other_checkbox7_edit.setChecked(False)

        #所有下拉式選單
        self.use_situation2_combobox_edit.setCurrentIndex(0)
        self.use_situation4_combobox_edit.setCurrentIndex(0)
        self.use_situation5_combobox_edit.setCurrentIndex(0)
        self.habit_combobox2_edit.setCurrentIndex(0)
        self.habit_combobox3_edit.setCurrentIndex(0)
        self.habit_combobox4_edit.setCurrentIndex(0)
        self.habit_combobox5_edit.setCurrentIndex(0)
        self.habit_combobox6_edit.setCurrentIndex(0)

    def toggle_send_button(self):
        # 根據 radio button 的選擇狀態啟用或禁用 send button
        self.introduction_send_pushButton.setEnabled(self.introduction_agree_radioButton.isChecked())    

    def submit_action(self):
        # 清除勾選框的選中狀態並禁用送出按鈕
        self.introduction_agree_radioButton.setChecked(False)
        self.introduction_send_pushButton.setEnabled(False)

    def cover_data_to_new_db(self):  # 編輯使用者介面 : Save按鍵更新使用者user_info
        user_name = self.nameBox_4.currentText()  # 從 UI 中取得使用者標識符

        # 查詢資料庫以檢查是否已經有該使用者的資料
        query_check = "SELECT * FROM user_info WHERE username = ?"
        self.cursorObj.execute(query_check, (user_name,))
        result = self.cursorObj.fetchone()

        if result:  # 如果找到該使用者資料則進行覆蓋            
            # 從 UI 中提取最新的數據
            name = self.name_input_edit.text()
            birthday = self.birthday_input_edit.text()

            # 性別
            if self.sex_man_button_edit.isChecked():
                gender = "男生"
            elif self.sex_women_button_edit.isChecked():
                gender = "女生"

                # 右眼狀況及度數設置
            right_eye_condition = "近視" if self.right_eye_in_button_edit.isChecked() else "遠視"
            right_eye_degree = self.right_eye_degree_input_edit.text()
            if right_eye_degree:
                right_eye_degree = -abs(float(right_eye_degree)) if right_eye_condition == "近視" else abs(float(right_eye_degree))
            right_eye_shine = "閃光" if self.right_eye_shine_button_edit.isChecked() else "無"
            right_eye_shine_degree = self.right_eye_shine_input_edit.text()

            # 左眼狀況及度數設置
            left_eye_condition = "近視" if self.left_eye_in_button_edit.isChecked() else "遠視"
            left_eye_degree = self.left_eye_degree_input_edit.text()
            if left_eye_degree:
                left_eye_degree = -abs(float(left_eye_degree)) if left_eye_condition == "近視" else abs(float(left_eye_degree))
            left_eye_shine = "閃光" if self.left_eye_shine_button_edit.isChecked() else "無"
            left_eye_shine_degree = self.left_eye_shine_input_edit.text()

            # 從按鈕組中提取 eye_situation 值
            eye_situation_value1 = self.eye_situation_button_group1_edit.checkedId()
            eye_situation_value2 = self.eye_situation_button_group2_edit.checkedId()
            eye_situation_value3 = self.eye_situation_button_group3_edit.checkedId()
            eye_situation_value4 = self.eye_situation_button_group4_edit.checkedId()
            eye_situation_value5 = self.eye_situation_button_group5_edit.checkedId()
            

            # 使用情況
            use_situation1 = "是" if self.use_situation_yes_button1_edit.isChecked() else "否"
            use_situation2 = self.use_situation2_combobox_edit.currentText()
            use_situation3 = "是" if self.use_situation_yes_button3_edit.isChecked() else "否"
            use_situation_value4 = self.use_situation4_combobox_edit.currentText()
            use_situation_value5 = self.use_situation5_combobox_edit.currentText()

            # 習慣值
            habit1 = "是" if self.habit_yes_button1_edit.isChecked() else "否"
            habit2 = self.habit_combobox2_edit.currentText()
            habit3 = self.habit_combobox3_edit.currentText()
            habit4 = self.habit_combobox4_edit.currentText()
            habit5 = self.habit_combobox5_edit.currentText()
            habit6 = self.habit_combobox6_edit.currentText()

            # 其他習慣（假設複選框）
            habit7 = []
            if self.habit_close_checkbox7_edit.isChecked():
                habit7.append("閉目養神")
            else:
                habit7.append("")
            if self.habit_exercise_checkbox7_edit.isChecked():
                habit7.append("眼部運動")
            else:
                habit7.append("")
            if self.habit_other_checkbox7_edit.isChecked():
                habit7.append("其他")
            else:
                habit7.append("")
            habit7_str = ",".join(habit7)  # 將多個習慣值連接成字串

            line_token = self.line_token_input_edit.text()

            self.cursorObj.execute('''
                INSERT INTO user_info (
                    name, username, birthday, gender, 
                    right_eye_condition, right_eye_degree, right_eye_shine, right_eye_shine_degree,
                    left_eye_condition, left_eye_degree, left_eye_shine, left_eye_shine_degree,
                    eye_situation_value1, eye_situation_value2, eye_situation_value3, eye_situation_value4, eye_situation_value5,
                    use_situation1, use_situation2, use_situation3, use_situation_value4, use_situation_value5,
                    habit1, habit2, habit3, habit4, habit5, habit6, habit7, line_token
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                name, user_name, birthday, gender, 
                right_eye_condition, right_eye_degree, right_eye_shine, right_eye_shine_degree,
                left_eye_condition, left_eye_degree, left_eye_shine, left_eye_shine_degree,
                eye_situation_value1, eye_situation_value2, eye_situation_value3, eye_situation_value4, eye_situation_value5,
                use_situation1, use_situation2, use_situation3, use_situation_value4, use_situation_value5,
                habit1, habit2, habit3, habit4, habit5, habit6, habit7_str, line_token
            ))

            # Commit the new data
            self.con.commit()

            # 彈跳式視窗提示
            save_data_msg_box = QMessageBox()
            save_data_msg_box.setWindowTitle("更新提示")
            save_data_msg_box.setText("已更新完畢")
            save_data_msg_box.setIcon(QMessageBox.Information)
            save_data_msg_box.setStandardButtons(QMessageBox.Ok)
            save_data_msg_box.buttonClicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
            save_data_msg_box.exec_()

            print(f"使用者 {user_name} 的資料已更新")
        else:
            print(f"找不到使用者 {user_name} 的資料，無法更新")

    def edit_delete_all(self):  # 編輯使用者介面 : 刪除使用者
        # 從下拉選單中獲取選中的使用者名稱
        user_identifier = self.nameBox_4.currentText()

        # 檢查該使用者是否存在於 database  中
        query_check = "SELECT * FROM user_info WHERE username = ?"
        self.cursorObj.execute(query_check, (user_identifier,))
        result = self.cursorObj.fetchone()

        # 彈出確認視窗
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("確認刪除")
        msg_box.setText(f"確定要刪除使用者 {user_identifier} 及其所有相關資料嗎？")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        # 獲取使用者的選擇
        reply = msg_box.exec_()

        if reply == QMessageBox.Yes:
            try:
                # 刪除 database 中的 user_info 資料
                query_delete = "DELETE FROM user_info WHERE username = ?"
                self.cursorObj.execute(query_delete, (user_identifier,))
                self.con.commit()
                print(f"已從 database 刪除使用者：{user_identifier} 的所有資料")

                # 刪除與該使用者相關的 posttest 表
                related_table_name = f"{user_identifier}_posttest"
                self.cursorObj.execute(
                    f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (related_table_name,))
                table_exists = self.cursorObj.fetchone()

                if table_exists:
                    self.cursorObj.execute(f"DROP TABLE IF EXISTS {related_table_name}")
                    self.con.commit()
                    print(f"已刪除與使用者 {user_identifier} 相關的 posttest 表: {related_table_name}")
                else:
                    print(f"沒有找到與使用者 {user_identifier} 相關的 posttest 表: {related_table_name}")

                # 刪除 database 中的 threshold 資料和使用者相關表格
                self.cursorObj = self.con.cursor()

                # 刪除 threshold 表中的使用者資料
                query_delete = "DELETE FROM threshold WHERE user = ?"
                self.cursorObj.execute(query_delete, (user_identifier,))
                self.con.commit()
                print(f"已從 database 的 threshold 表中刪除使用者：{user_identifier}")

                # 刪除與該使用者相關的表（假設表名與使用者名稱一致）
                related_table_name_db = user_identifier  # 假設數據表的名稱與使用者名稱一致
                self.cursorObj.execute(
                    f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (related_table_name_db,))
                table_exists_db = self.cursorObj.fetchone()

                if table_exists_db:
                    self.cursorObj.execute(f"DROP TABLE IF EXISTS {related_table_name_db}")
                    self.con.commit()
                    print(f"數據表 {related_table_name_db} 已從 database 中刪除。")
                else:
                    print(f"數據表 {related_table_name_db} 不存在，無需刪除。")

            except sqlite3.Error as e:
                print(f"刪除 database 或 database 中使用者或相關表時發生錯誤: {e}")

            # 從 nameBox 中移除使用者名稱
            for box in [self.nameBox, self.nameBox_2, self.nameBox_3, self.nameBox_4]:
                index = box.findText(user_identifier)
                if index >= 0:
                    box.removeItem(index)

            # 返回首頁
            self.stackedWidget.setCurrentIndex(0)
            print("刪除操作已完成，返回首頁。")

        else:
            print("刪除操作已取消")

    def add_user_onchange(self):
        pass

    def camera_onchange(self):
        print(f"camera_onchange中的current_user {self.current_user}")

        self.create_user_data()
        self.start_time = time.time()
        self.status = 'run'
        self.camera = cv.VideoCapture(0)
        self.timer_camera.start(5)
        self.timer_warm.start(30)
        self.camera_active = True
        self.start.setEnabled(True)
        self.line_token = self.token
        self.suggestion.setEnabled(True)
        self.login1_homebutton.setEnabled(False)
        #self.current_user = str(self.nameBox_2.currentText())  # Fetch current selected user from nameBox_2

        self.update_progress_value()
        # Get the current user
        #self.current_user = str(self.nameBox_2.currentText())  # Fetch current selected user from nameBox_2
        
        
        # Get the current threshold values
        distance_ratio = self.distance_th.value()
        brightness = self.bright_th.value()
        blink = self.blink_th.value()

        # Log the values for debug purposes (can remove in production)
        print(f"Distance Ratio: {distance_ratio}, Brightness: {brightness}, Blink: {blink}")

        # Update the database with the new threshold values
        try:
            self.cursorObj.execute('''
                UPDATE threshold 
                SET distance_ratio = ?, brightness = ?, blink = ? ,blink_num=?
                WHERE user = ?
            ''', (distance_ratio, brightness, blink, self.current_user))

            # Commit the changes to the database
            self.con.commit()
            print(f"Threshold values updated for user {self.current_user}")

        except sqlite3.Error as e:
            print(f"Error updating threshold: {e}")
        
    def start_push_onchange(self): 
        self.work_time = self.working_time.value()
        self.processing_images = True #圖片處理應開始執行
        print("開始圖片處理")
        print(f"start_push_onchange中的current_user: {self.current_user}")
        print("start_push_onchange中的nameBox_2:",str(self.nameBox_2.currentText()))

        # 獲取當前時間並轉為適合儲存的格式
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 查詢 user_info 表中 start_time_for_database 欄位的最新值是否為空
        self.cursorObj.execute('SELECT start_time_for_database FROM user_info ORDER BY id DESC LIMIT 1')
        latest_record = self.cursorObj.fetchone()

        if latest_record and not latest_record[0]:  # 如果為空值，插入當前時間
            self.cursorObj.execute(
                'UPDATE user_info SET start_time_for_database = ? WHERE id = (SELECT MAX(id) FROM user_info)',
                (current_time,)
            )
            self.con.commit()  # 提交更改
            print("start_time_for_database 欄位已更新為當前時間:", current_time)
        else:
            print("start_time_for_database 欄位已有值，無需更新")

        # 剩餘的邏輯
        self.start_time_for_database = current_time
        self.line_token_input.setText(self.token)
        self.lineNotifyMessage('start')  # 發送 LINE 通知
        # 其他相關變數初始化
        self.counter = -1
        self.pass_time = 0.01
        self.status = 'start'
        self.time_status = 'work'
        self.previous_minute = 0
        self.init_time = time.time()
        self.previous_time_step = time.time()
        self.camera_active = False
        self.login2_homebutton.setEnabled(False)

        # 初始化相機
        self.camera = cv.VideoCapture(0)  # 根據需要更改索引
        # 設定提醒邏輯
        if self.weighted_average  < self.work_time and self.weighted_average != 0 :
            reminder_time = self.weighted_average
            print(f"開始計時，將在 {reminder_time} 分鐘後提醒用戶休息。")
            self.schedule_reminder(reminder_time)
        elif self.weighted_average == 0 :
            print(f" 沒有資料提供預測，無需提醒。")

        else:
            print(f"用戶設置的工作時間小於等於預測時間 {self.weighted_average:.0f} 分鐘，無需提醒。")

         # 確保相機已經啟動
        if self.camera.isOpened():
            print("相機已啟動，但未開始截圖")
            self.timer_camera.start(100)  # 每 100 毫秒捕獲一次
            # 手動觸發捕獲方法進行測試
            self.capture_camera_frame()
             # 啟動圖片處理
            self.process_images()
            print("圖片處理已啟動")
        else:
            print("相機未啟動")

    def capture_camera_frame(self, save_path=None):
        # 獲取當前程式碼所在的資料夾路徑
        base_path = os.path.dirname(os.path.abspath(__file__))

        # 父資料夾名稱
        parent_folder = "photos"
        parent_path = os.path.join(base_path, parent_folder)

        # 檢查父資料夾是否存在，並進行創建
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)  # 創建父資料夾


        # 根據狀態選擇保存資料夾，並設置為父資料夾下的子資料夾
        if self.is_exhausted:
            save_path = os.path.join(parent_path, "exhausted")
        else:
            save_path = os.path.join(parent_path, "normal")
        
        # 檢查子資料夾是否存在，並進行創建
        if not os.path.exists(save_path):
            os.makedirs(save_path)  # 創建子資料夾


        # 判斷當前的狀態
        #current_state = "exhausted" if self.is_exhausted else "normal"  # 根據是否疲勞狀態決定狀態名稱


        if  self.status == 'start' and self.camera is not None and self.camera.isOpened():
            ret, frame = self.camera.read()  # 從相機捕獲圖像幀
            if ret:
            # 生成文件名並保存截圖
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]  
                filename = os.path.join(save_path, f"{timestamp}_camera.jpg")
                cv.imwrite(filename, frame, [cv.IMWRITE_JPEG_QUALITY, 70])  # 調整品質以減少檔案大小
                print(f"Screenshot saved: {filename}")

                # 使用線程進行數據記錄
                threading.Thread(target=self.save_data, args=(save_path, timestamp, filename,frame)).start()

    def save_data(self, save_path, timestamp, filename,frame):

        brightness_value = self.brightness_value
        blink_count = self.blink_per_minute
        current_state = "exhausted" if self.is_exhausted else "normal"

        # 使用 MediaPipe 偵測臉部
        results = self.face_detection.process(frame)

        face_area = 0
        ellipse_params = None

        if results.detections:
            for detection in results.detections:
                # 計算臉部的矩形區域
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                # 計算臉部面積
                face_area = w * h

                # 在圖片上繪製矩形框
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # 計算拖元：擬合椭圆
                roi = frame[y:y+h, x:x+w]
                if roi.shape[0] > 0 and roi.shape[1] > 0:
                    gray_roi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
                    _, binary_roi = cv.threshold(gray_roi, 30, 255, cv.THRESH_BINARY)
                    contours, _ = cv.findContours(binary_roi, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

                    if contours:
                        # 找到最大輪廓並擬合椭圆
                        largest_contour = max(contours, key=cv.contourArea)
                        if len(largest_contour) >= 5:
                            ellipse = cv.fitEllipse(largest_contour)
                            cv.ellipse(frame, ellipse, (0, 255, 0), 2)
                            ellipse_params = ellipse  # 取得椭圆的參數

                            # 提取椭圆的參數：中心點、長軸、短軸和角度
                            center = tuple(map(int, ellipse[0]))
                            axes = tuple(map(int, ellipse[1]))
                            angle = ellipse[2]

                # 計算長軸和短軸的端點
                            angle_rad = np.deg2rad(angle)  # 角度轉換為弧度
                            long_axis_length = axes[0] / 2  # 長軸半徑
                            short_axis_length = axes[1] / 2  # 短軸半徑

                # 長軸端點
                            long_axis_end_x = int(center[0] + long_axis_length * np.cos(angle_rad))
                            long_axis_end_y = int(center[1] + long_axis_length * np.sin(angle_rad))
                # 短軸端點
                            short_axis_end_x = int(center[0] - short_axis_length * np.sin(angle_rad))
                            short_axis_end_y = int(center[1] + short_axis_length * np.cos(angle_rad))

                # 繪製長軸（綠色線條）
                            cv.line(frame, center, (long_axis_end_x, long_axis_end_y), (0, 255, 0), 2)

                # 繪製短軸（藍色線條）
                            cv.line(frame, center, (short_axis_end_x, short_axis_end_y), (255, 0, 0), 2)


                    

            # 記錄數據（亮度和眨眼次數）
            # 初始化累積的數據列表
        data = {
                "timestamp": timestamp,
                "brightness": brightness_value,
                "blink_count": blink_count,
                "state": current_state,
                "face_area": face_area,
                "ellipse_params": {
                "long_axis": long_axis_length * 2,  # 完整的長軸長度（不僅是半徑）
                "short_axis": short_axis_length * 2,
                "angle": ellipse_params[2] if ellipse_params else None
                }
            }
        

            # 統一保存 JSON 檔案為固定名稱
        json_filename = os.path.join(save_path, "latest_data.json")
            # 如果 JSON 檔案已存在，讀取舊數據，否則初始化為空列表
        if os.path.exists(json_filename):
            with open(json_filename, 'r') as json_file:
                data_list = json.load(json_file)
        else:
            data_list = []

            # 將新數據附加到數據列表
        data_list.append(data)

            # 保存累積數據到 JSON 文件
        with open(json_filename, 'w') as json_file:
            json.dump(data_list, json_file, indent=4)

        print(f"Data saved to: {json_filename}")
            
            # 生成 JSON 文件名
            #json_filename = os.path.join(save_path, f"{timestamp}_data.json")
            
            # 保存數據到 JSON 文件
            #self.data_list.append(data)  # 把當前數據加入數據列表
           # with open(json_filename, 'w') as json_file:
                #json.dump(self.data_list, json_file, indent=4)

    def compress_image(self, image_path):
        """壓縮圖片並保存為 JPG 格式"""
        try:
            img = Image.open(image_path)
            compressed_path = image_path.replace('.png', '_compressed.jpg')
            img.save(compressed_path, 'JPEG', quality=70)  # 調整品質以減少檔案大小
            print(f"Compressed image saved: {compressed_path}")
        except Exception as e:
            print(f"Error compressing image: {e}")




    #新增Exhausted
    def pushButton_Exhausted_onchange(self):
        current_time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime())  # 獲取當前時間，精確到分鐘
        
        # 檢查是否在同一分鐘內重複按下
        if hasattr(self, 'last_exhausted_time_str') and self.last_exhausted_time_str == current_time_str:
            self.showMainWindow("You cannot press the button again within the same minute.", line=False)
            return

        # 更新上次按下的時間
        self.last_exhausted_time_str = current_time_str

        if self.status in ['start', 'rest']:  
            if not self.is_exhausted:  # 第一次按下，進入疲勞狀態
                self.Exhausted_state = 0  # 設置疲勞狀態為 1
                self.Exhausted_count = 1
                self.is_exhausted = True
                self.pushButton_Exhausted.setStyleSheet("background-color: yellow")  # 標記按鈕狀態
                # 顯示 "開始" 在小白板
                if self.last_time_recorded != current_time_str:
                    item = QtGui.QStandardItem(f"  {current_time_str} 開始")
                    self.listView_model.appendRow(item)
                    self.last_time_recorded = current_time_str
                    self.capture_interval = 100
                    self.timer_camera.start(self.capture_interval)  # 開始定時器，定期截圖
                    

                message = "You entered exhausted state. Do you want to rest?"
                self.showConfirmationDialog(message, self.handle_rest_decision)

            #else:  # 如果已經在疲勞狀態，則保持狀態
                #self.showMainWindow("You are already in exhausted state.", line=False)

            else:
                #self.is_exhausted:  # 第二次按下按鈕，恢復正常狀態
                self.Exhausted_state = 0  # 重置疲勞狀態為0
                self.Exhausted_count = 0
                self.is_exhausted = False
                self.pushButton_Exhausted.setStyleSheet("")  # 移除按鈕狀態

                # 顯示 "結束" 在小白板
                if self.last_time_recorded != current_time_str:
                    item = QtGui.QStandardItem(f"  {current_time_str} 結束")
                    self.listView_model.appendRow(item)
                    self.last_time_recorded = current_time_str
                #self.showMainWindow("Exhausted state ended", line=False)
        else:
            self.showMainWindow("Cannot change to exhausted state during shutting down")


    def showConfirmationDialog(self, message, callback):
        # 創建訊息對話框
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Confirmation')
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        # 設置窗口保持在最前方
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
        
        reply = msg_box.exec_()
        
        # 根據回應呼叫對應的回調
        if reply == QMessageBox.Yes:
            callback('yes')
        else:
            callback('no')

    def handle_rest_decision(self, choice):
        if choice == 'yes':
            # 使用者選擇休息，進入休息狀態
            self.status = 'rest'
            self.record_state = 0  # 設置為休息狀態
            self.pass_time = 0  # 重置計時
            self.previous_time_step = time.time()  # 更新時間基準
            #self.showMainWindow("結束工作狀態，進入休息狀態", line=False)
        else:
            # 使用者選擇繼續工作，保持疲勞狀態
            self.is_exhausted = True           
            # 顯示仍處於疲勞狀態的消息
            #self.showMainWindow("Continuing to work in exhausted state", line=False)
    def handle_rest_decision_predict(self, choice):
        #這邊是因為我不想更改處理的邏輯，直接新增一個相似的函數來處理預測時間到達使用者的決定 BY ryan
        if choice == 'yes':
            # 使用者選擇休息，進入休息狀態
            self.status = 'rest'
            self.record_state = 0  # 設置為休息狀態
            self.pass_time = 0  # 重置計時
            self.previous_time_step = time.time()  # 更新時間基準
            #self.showMainWindow("結束工作狀態，進入休息狀態", line=False)
        else:
            print("用戶選擇繼續工作，忽略預測工作時間提醒。")    
    def next_rest_decision(self, choice):
        if choice == 'yes':
            # 使用者選擇休息，進入休息狀態
            self.status = 'rest'
            self.record_state = 0  # 設置為休息狀態
            self.pass_time = 0  # 重置計時
            self.previous_time_step = time.time()  # 更新時間基準
            #self.showMainWindow("結束工作狀態，進入休息狀態", line=False)
            self.next_threshold = 10  # 重置詢問閾值回到10分鐘
        else:
            # 使用者選擇繼續工作，保持疲勞狀態
            self.is_exhausted = True
            
            # 根據規則減少下一次彈窗的間隔
            # 第一次間隔 8 分鐘，之後每次間隔減少 2 分鐘
            if self.next_threshold == 15:
                self.next_threshold += 10
            else:
                self.next_threshold += 5
            
            # 顯示仍處於疲勞狀態的消息
            #self.showMainWindow("Continuing to work in exhausted state", line=False)


    def finish_push_onchange(self): 
        self.last_exhausted_time_str = 0
        self.time_status = 'finished'
        self.status = 'shutting_down'
        self.is_running = False  # 停止推理運行
        self.release_resources()  # 釋放與推理相關的資源
        logging.getLogger('tensorflow').setLevel(logging.ERROR)  # 停止時只顯示錯誤級別的日誌
        """ 停止圖片處理 """
        self.processing_images = False
        print("圖片處理已停止")        # 關閉相機和停止推理
        if self.camera is not None:
            self.camera.release()

        # 清空 camera_site 和 camera_site_2 的畫面
        empty_frame = QPixmap(800, 600)  # 創建一個空白的畫面
        empty_frame.fill(Qt.white)  # 設置背景為黑色或其他顏色
        self.camera_site.setPixmap(empty_frame)  # 清空顯示區域
        self.camera_site_2.setPixmap(empty_frame)  # 清空副顯示區域

        # 重置疲勞按鈕狀態
        self.is_exhausted = False  # 將疲勞狀態設置為初始狀態
        self.start.setEnabled(False) 
        self.suggestion.setEnabled(False)
        self.Exhausted_state = 0  # 重置疲勞狀態變量
        self.pushButton_Exhausted.setStyleSheet("")  # 移除反黃顯示

        # 清空小白板（ListView）的內容
        self.listView_model.clear()  # 清除小白板中所有條目
        self.last_time_recorded = None  # 重置最後記錄的時間
        self.switch_page(6)  #page2 按下Finish 跳轉至page6填寫後測


    def run_inference(self):
        # 執行推理過程的函數
        if not self.is_running:
            return  # 停止推理
        # 進行推理的代碼


    def release_resources(self):
        '''# 如果有模型需要釋放，檢查模型是否存在
        if hasattr(self, 'model') and self.model is not None:
            del self.model'''
    
        # 如果有 session 或推理進程
        if hasattr(self, 'session') and self.session is not None:
            self.session.close()

        print("所有推理相關資源已釋放")


    def calendar(self):
        selectDay = self.calendarWidget.selectedDate()
        year = selectDay.toString("yyyy")
        month = selectDay.toString("M")
        day = selectDay.toString("d")
        selected_date = selectDay.toString('yyyy-MM-dd')
        print(year, month, day)

        self.cursorObj = self.con.cursor()

        cursor = self.cursorObj.execute(
            f"SELECT year, month, day, hour, minute, distance, brightness, blink, state, Exhausted_state "
            f"FROM {self.current_user}_data WHERE year=? AND month=? AND day=? ORDER BY hour, minute",
            (year, month, day)
        )        
        self.con.commit()
        date = []
        dis = []
        bri = []
        blink = []
        use = []
        for i in cursor:
            date.append(datetime(i[0], i[1], i[2], i[3], i[4]))
            use.append(i[8])
            dis.append(float(i[5]))
            bri.append(int(i[6]))
            blink.append(int(i[7]))
        
        xfmt = matplotlib.dates.DateFormatter('%H:%M')
        datestime = matplotlib.dates.date2num(date)

        # 1. 使用時間圖表
        plt.gca().xaxis.set_major_formatter(xfmt)
        plt.plot_date(datestime, use, linestyle='solid')
        plt.yticks([0, 1, 2], ['rest', 'absent', 'work'])        
        plt.ylim(-0.1, 2.1)
        plt.title('Using Time')
        plt.xlabel('Time')  # 新增 X 軸標題
        plt.ylabel('Activity State')  # Y 軸標題
        plt.text(1.0, 1.05, selected_date, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')
        plt.savefig('use.png')
        plt.close()

        # 顯示圖片
        self.display_image(cv.imread('use.png'), (400, 270), self.use_time_graph)

        # 2. 距離圖表
        plt.gca().xaxis.set_major_formatter(xfmt)
        plt.plot_date(datestime, dis, linestyle='solid')
        plt.yticks([0.5,1.5, 2.5], ['too close', 'normal','too far'])
        plt.ylim(0, 3)
        plt.title('Distance')
        plt.xlabel('Time')  # 新增 X 軸標題
        plt.ylabel('Viewing Distance')  # Y 軸標題
        plt.text(1.0, 1.05, selected_date, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')
        plt.savefig('dis.png')
        plt.close()

        # 顯示圖片
        self.display_image(cv.imread('dis.png'), (400, 270), self.distance_graph)

        # 3. 環境亮度圖表
        plt.gca().xaxis.set_major_formatter(xfmt)
        plt.plot_date(datestime, bri, linestyle='solid')
        plt.yticks([100, 120, 200, 255], ['dark', 'normal', 'adequate', 'too light'])

        plt.ylim(0, 255)
        plt.title('Brightness')
        plt.xlabel('Time')  # 新增 X 軸標題
        plt.ylabel('Brightness Level')  # Y 軸標題
        plt.text(1.0, 1.05, selected_date, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')
        plt.savefig('bri.png')
        plt.close()

        # 顯示圖片
        self.display_image(cv.imread('bri.png'), (400, 270), self.brightness_graph)

        # 4. 每分鐘眨眼次數圖表
        plt.gca().xaxis.set_major_formatter(xfmt)
        plt.plot_date(datestime, blink, linestyle='solid')
        plt.ylim(0, 60)
        plt.title('Blinking')
        plt.xlabel('Time')  # 新增 X 軸標題
        plt.ylabel("Blink Count")
        plt.text(1.0, 1.05, selected_date, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')
        plt.savefig('blink.png')
        plt.close()

        # 顯示圖片
        self.display_image(cv.imread('blink.png'), (400, 270), self.blink_graph)

    def send_images_to_line(self):
        """
        發送日期文字訊息和四張圖片到 LINE Notify，每張圖片附帶不同訊息
        """

        # 1. 取得當日日期並發送文字訊息
        selectDay = self.calendarWidget.selectedDate()
        selected_date = selectDay.toString('yyyy-MM-dd')  # 將選擇的日期格式化為 'yyyy-MM-dd'
        message = f"以下為 {selected_date} 的用眼分析報表"

        try:
            # 發送文字訊息到 LINE Notify
            headers = {
                "Authorization": "Bearer " + self.token,  # 使用存儲的 token
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {'message': message}
            
            # 發送 POST 請求傳送訊息
            r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)

            if r.status_code == 200:
                print("Text message sent successfully.")
            else:
                print(f"Failed to send text message. Status code: {r.status_code}")
        except Exception as e:
            print(f"Error sending text message: {e}")
            return  # 如果發送訊息失敗，就不進行後續的圖片傳送

        # 2. 發送四張圖片，每張圖片有不同的訊息
        # 2. 發送四張圖片，每張圖片有不同的訊息
        image_files = ['use.png', 'dis.png', 'bri.png', 'blink.png']
        image_messages = [
            f'{selected_date}當日使用時間',  # 對應 use.png
            f'{selected_date}當日距離',      # 對應 dis.png
            f'{selected_date}當日環境亮度',  # 對應 bri.png
            f'{selected_date}當日眨眼情形'  # 對應 blink.png
        ]

        for image_file, image_message in zip(image_files, image_messages):
            try:
                # 開啟圖片檔案並以二進位方式讀取
                with open(image_file, 'rb') as image:
                    image_headers = {
                        "Authorization": "Bearer " + self.token,  # 使用存儲的 token
                    }

                    # 傳送每張圖片時附帶對應的訊息
                    image_data = {'message': image_message}

                    # 發送 POST 請求到 LINE Notify 並附上圖片和訊息
                    files = {'imageFile': image}
                    r = requests.post("https://notify-api.line.me/api/notify", headers=image_headers, data=image_data, files=files)

                    if r.status_code == 200:
                        print(f"Image {image_file} sent successfully with message: {image_message}")
                    else:
                        print(f"Failed to send {image_file}. Status code: {r.status_code}")
            except Exception as e:
                print(f"Error sending {image_file}: {e}")
    
    def display_image(self, img, size, target):
        if img is None:
            print("Error: Could not load image.")
            return
    
        resized_image = cv.resize(img, size)
        # 將圖像轉換為 QImage 格式
        height, width, channel = resized_image.shape
        bytesPerLine = 3 * width
        q_img = QImage(resized_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
    
        pixmap = QPixmap.fromImage(q_img)
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
    
        target.setScene(scene)
        target.fitInView(scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def add_push_onchange(self):
        # 獲取使用者輸入的名稱
        text = str(self.user_name_input.text())

        # 檢查名稱是否為空
        if text == '':
            print('名稱為空，無法新增')
            return  # 名稱為空，直接返回

        # 檢查名稱是否已經存在於下拉選單中
        for i in range(self.nameBox.count()):
            if self.nameBox.itemText(i) == text:
                print(f'名稱 "{text}" 已經存在，無法新增')
                return  # 名稱已存在，直接返回

        # 名稱有效且未重複，新增到下拉選單
        self.nameBox.addItem(text)
        self.nameBox_2.addItem(text)
        self.nameBox_3.addItem(text)
        self.nameBox_4.addItem(text)
        self.current_user  = str(self.nameBox_2.currentText())
        if (text != ''):
            self.con = sqlite3.connect(self.db_path)
            self.cursorObj = self.con.cursor()

            try:
                self.cursorObj.execute(f'''CREATE TABLE IF NOT EXISTS {self.current_user}_data (year, month, day, hour, minute, distance, brightness, blink, state, Exhausted_state,start_time_for_database)''' )
                self.cursorObj.execute(f'''
                    CREATE TABLE IF NOT EXISTS {self.current_user}_posttest (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question_1 TEXT,
                        question_2 TEXT,
                        question_3 TEXT,
                        question_4 TEXT,
                        question_5 TEXT,
                        question_6 TEXT,        
                        question_7 INTEGER,
                        question_8 INTEGER,
                        question_9 INTEGER,
                        question_10 INTEGER,
                        question_11 INTEGER,
                        question_12 TEXT,
                        submission_time TEXT,
                        start_time_for_database TEXT
                    );
                ''')
                self.cursorObj.execute("insert or ignore into threshold(user,line_token,  distance_area, distance_ratio, brightness, blink,blink_num) VALUES (?,?,?,?,?,?,?)" ,(text,self.line_token_input.text(),self.eye_area_record,self.eye_area_ratio,60,4,15))
                self.con.commit()
            except:
                self.showMainWindow('Not valid name!')
        else:
            print('empty')


    def working_time_onchange(self):
        """
        當用戶手動調整工作時間時記錄變更，但不啟動提醒。
        """
        try:
            # 從 UI 控件讀取當前設置的工作時間
            self.work_time = self.working_time.value()
            #self.manual_work_time = self.work_time
            #print(f"用戶手動設置工作時間為 {self.manual_work_time} 分鐘。")

            # 僅記錄時間，不啟動提醒
            if self.work_time > self.weighted_average:
                print(f"用戶設置時間 {self.work_time} 分鐘超過疲勞預測值 {self.weighted_average} 分鐘。")
            else:
                print(f"用戶設置時間 {self.work_time} 分鐘未超過疲勞預測值 {self.weighted_average} 分鐘。")
        except Exception as e:
            print(f"手動調整工作時間失敗：{e}")



    def schedule_reminder(self, time_to_remind):
        """
        啟動提醒計時器，僅在 weighted_average 小於 work_time 時調用。
        """
        try:
            print(f"設定計時器，{time_to_remind:.0f} 分鐘後提醒用戶休息。")
            
            # 啟動計時器到提醒時間
            QTimer.singleShot(int(time_to_remind * 60 * 1000), self.show_rest_reminder)

        except Exception as e:
            print(f"設定提醒失敗：{e}")



    def show_rest_reminder(self):
        """
        顯示休息提醒窗口，讓用戶選擇是否進入休息狀態。
        """
        try:
            message = (
                f"<p style='font-size:20px; font-weight:bold; color:#808080;'>⏰ 疲勞提醒！<span style='font-size:20px; font-weight:bold; color:#808080;'> 是否進入休息狀態？</span></p>"
                f"<p style='font-size:16px; font-weight:bold; color:#808080;'>您已經工作了 <span style='font-size:22px; font-weight:bold; color:#3D5A80;'> {self.weighted_average:.0f} 分鐘</span> </p>"
                f"<p style='font-size:16px; font-weight:bold; color:#808080;'>建議休息 5 分鐘，放鬆一下再繼續！😊</p>"
            )
            self.showConfirmationDialog(message, self.handle_rest_decision_predict)

        except Exception as e:
            print(f"顯示提醒窗口失敗：{e}")

    def resting_time_onchange(self):
        self.rest_time = self.resting_time.value()

    def suggestion_push_onchange(self):
        br = 4.0
        bv = 100
        dis = 0.7
        self.blink_th.setValue(br)
        self.bright_th.setValue(bv)
        self.distance_th.setValue(dis)
        self.eye_area_record = self.eye_area
        self.update_database()
    
    def update_database(self):
        query = "UPDATE threshold SET distance_area = ?, distance_ratio = ?, brightness = ?, blink = ?,blink_num=? WHERE user = ?"
        
        # 更新第一組閾值
        self.cursorObj.execute(query, (self.eye_area, self.distance_th.value(), self.bright_th.value(), self.blink_th.value(), self.blink_num_th_2.value(), self.current_user))
        
        # 更新第二組閾值
        self.cursorObj.execute(query, (self.eye_area, self.distance_th_2.value(), self.bright_th_2.value(), self.blink_th_2.value(), self.blink_num_th_2.value(), self.current_user))
        
        self.con.commit()


    def check_status(self):     #太近/太暗警示
        if (self.status == 'start'):
            if(self.area_counter>2):
                self.showMainWindow('Too close',line=True)

                self.area_counter = 0
            if(self.bright_counter >20):
                self.showMainWindow('Too dim')
                self.bright_counter = 0
        

    ''' eye detection function '''

    def PolyArea(self,x,y):
        return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

    # landmark detection function 
    def landmarksDetection(self,img, results, draw=False,body=False):
        img_height, img_width= img.shape[:2]
        # list[(x,y), (x,y)....]
        if(body==False):
            mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
        else:
            mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.pose_world_landmarks.landmark]
        if draw :
            [cv.circle(img, p, 2, (0,255,0), -1) for p in mesh_coord]
        # returning the list of tuples for each landmarks 
        return mesh_coord

    # Euclaidean distance 
    def euclaideanDistance(self,point, point1):
        x, y = point
        x1, y1 = point1
        distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
        return distance

    def blinkRatio(self,img, landmarks, right_indices, left_indices):
        # Right eyes 
        # horizontal line 
        rh_right = landmarks[right_indices[0]]
        rh_left = landmarks[right_indices[8]]
        # vertical line 
        rv_top = landmarks[right_indices[12]]
        rv_bottom = landmarks[right_indices[4]]
        # draw lines on right eyes 
        # LEFT_EYE 
        # horizontal line 
        lh_right = landmarks[left_indices[0]]
        lh_left = landmarks[left_indices[8]]
        # vertical line 
        lv_top = landmarks[left_indices[12]]
        lv_bottom = landmarks[left_indices[4]]
        rhDistance = self.euclaideanDistance(rh_right, rh_left)
        rvDistance = self.euclaideanDistance(rv_top, rv_bottom)
        lvDistance = self.euclaideanDistance(lv_top, lv_bottom)
        lhDistance = self.euclaideanDistance(lh_right, lh_left)
        reRatio = rhDistance/rvDistance
        leRatio = lhDistance/lvDistance
        ratio = (reRatio+leRatio)/2
        return ratio 

    def get_average_brightness(self,image,mesh_coords,frame_height,frame_width):
        lum = image[:,:,0]*0.144+image[:,:,1]*0.587+image[:,:,2]*0.299
        vals = np.average(lum)
        if math.isnan (vals) :
            return 0
        else:
            return vals

    def colorBackgroundText(self,img, text, font, fontScale, textPos, textThickness=1,textColor=(0,255,0), bgColor=(0,0,0), pad_x=3, pad_y=3):
        (t_w, t_h), _= cv.getTextSize(text, font, fontScale, textThickness) # getting the text size
        x, y = textPos
        cv.rectangle(img, (x-pad_x, y+ pad_y), (x+t_w+pad_x, y-t_h-pad_y), bgColor,-1) # draw rectangle 
        cv.putText(img,text, textPos,font, fontScale, textColor,textThickness ) # draw in text

        return img

    def showMainWindow(self,text,line=True):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(text)
        msgBox.setWindowTitle("Warning")
        # 設置視窗為最前顯示
        msgBox.setWindowFlags(msgBox.windowFlags() | Qt.WindowStaysOnTopHint)

        msgBox.exec()
        #if (line and self.want_line.isChecked()):
        #self.lineNotifyMessage(text)

    def get_state_body(self,results):
        up_state = 1
        down_state = -1
        left_wrist = results.pose_world_landmarks.landmark[15]
        left_pinky = results.pose_world_landmarks.landmark[17]
        right_wrist = results.pose_world_landmarks.landmark[16]
        right_pinky =  results.pose_world_landmarks.landmark[18]
        left_hip = results.pose_world_landmarks.landmark[23]
        right_hip = results.pose_world_landmarks.landmark[24]
        nose = results.pose_world_landmarks.landmark[0]
        if(left_wrist.y < nose.y and right_wrist.y < nose.y):
            return up_state
        elif(left_pinky.y > left_hip.y and right_pinky.y > right_hip.y):
            return down_state
        return 0

    def update_progress_value(self):
        try:  
            #self.current_user = str(self.nameBox_3.currentText())  # Fetch current selected user from nameBox_2
            print(f"update_progress_value當前使用者: {self.current_user}, blink_per_minute: {self.blink_per_minute}")
            if(self.status != 'rest' and self.status != 'shutting_down'):
                with self.map_face_mesh.FaceMesh(min_detection_confidence =0.5, min_tracking_confidence=0.5) as face_mesh:
                    self.frame_counter += 1
                    ret, frame = self.camera.read() 
                    frame_height, frame_width= frame.shape[:2]
                    rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
                    results  = face_mesh.process(rgb_frame)
                    FONT = cv.FONT_HERSHEY_COMPLEX

                    ###
                    if results.multi_face_landmarks:
                        #self.record_state = 0
                        if(self.status == 'start'):
                            self.time_status = 'work'
                        mesh_coords = self.landmarksDetection(frame, results, False)
                        right_eye_area = self.PolyArea(np.array([mesh_coords[p] for p in self.RIGHT_EYE ])[:,0],np.array([mesh_coords[p] for p in self.RIGHT_EYE ])[:,1])
                        left_eye_area = self.PolyArea(np.array([mesh_coords[p] for p in self.LEFT_EYE ])[:,0],np.array([mesh_coords[p] for p in self.LEFT_EYE ])[:,1])
                        self.eye_area = (right_eye_area+left_eye_area)/2
                        self.ratio = self.blinkRatio(frame, mesh_coords, self.RIGHT_EYE, self.LEFT_EYE)
                        self.brightness_value = self.get_average_brightness(rgb_frame,mesh_coords,frame_height,frame_width) 
                        # 觸發截圖
                        self.capture_camera_frame()

                        #self.eyestate = 0  # **初始化為未眨眼**
                        if self.camera_active:
                            if self.ratio > self.blink_th.value(): #close eye
                                self.colorBackgroundText(frame,  f'Blink', FONT, self.FONT_SIZE, (int(frame_height/2), 100), 2, (0,255,255), pad_x=6, pad_y=6, )

                            if (self.eye_area_record/self.eye_area)**0.5 < self.distance_th.value():
                                        self.showMainWindow('Too close',line=True)


                            if self.brightness_value <self.bright_th.value():
                                    self.colorBackgroundText(frame,  f'Too dim', FONT, self.FONT_SIZE, (int(frame_height/2), 150), 2, (0,255,255), pad_x=6, pad_y=6, )                           

                        cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.LEFT_EYE ], dtype=np.int32)], True,(0,255,0), 1, cv.LINE_AA)
                        cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.RIGHT_EYE ], dtype=np.int32)], True, (0,255,0), 1, cv.LINE_AA)
                        cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.FACE_OVAL ], dtype=np.int32)], True, (0,0,255), 1, cv.LINE_AA)
                    else:
                        self.record_state = 1 # do not detect people
                    self.fps_pass_time = time.time()-self.start_time
                    fps = self.frame_counter/self.fps_pass_time
                    self.colorBackgroundText(frame,  f'Eye area : {(self.eye_area)}', FONT, self.FONT_SIZE/2, (30,90),1)
                    self.colorBackgroundText(frame,  f'Eye Distance ratio: {round((self.eye_area_record/self.eye_area)**0.5,2)}', FONT, self.FONT_SIZE/2, (30,120),1)
                    self.colorBackgroundText(frame,  f'Eye Ratio: {round(self.ratio,2)}', FONT, self.FONT_SIZE/2, (30,150),1)
                    self.colorBackgroundText(frame,  f'Brightness: {round(self.brightness_value,1)}', FONT, self.FONT_SIZE/2, (30,180),1)
                    self.colorBackgroundText(frame,  f'FPS: {round(fps,1)}', FONT,self.FONT_SIZE/2, (30,60),1)
                    self.colorBackgroundText(frame,  f'status: {self.status}', FONT, self.FONT_SIZE/2, (30,420),1)
                    self.colorBackgroundText(frame,  f'time.status: {self.time_status}', FONT, self.FONT_SIZE/2, (30,390),1)
                    self.colorBackgroundText(frame,  f'record_state: {self.record_state}', FONT, self.FONT_SIZE/2, (30,360),1) 

                    show = cv.resize(frame,(800,600))
                    show = cv.cvtColor(show, cv.COLOR_BGR2RGB)
                    showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
                    self.camera_site.setPixmap(QPixmap.fromImage(showImage))

                    if results.multi_face_landmarks:
                        self.record_state = 2
                        if (self.time_status == 'work'):
                            self.pass_time += (time.time() - self.previous_time_step)
                            self.previous_time_step =  time.time()
                        else:
                            self.pass_time += 0
                        if(self.status == 'start'):
                            self.time_status = 'work'
                        mesh_coords = self.landmarksDetection(frame, results, False)
                        right_eye_area = self.PolyArea(np.array([mesh_coords[p] for p in self.RIGHT_EYE ])[:,0],np.array([mesh_coords[p] for p in self.RIGHT_EYE ])[:,1])
                        left_eye_area = self.PolyArea(np.array([mesh_coords[p] for p in self.LEFT_EYE ])[:,0],np.array([mesh_coords[p] for p in self.LEFT_EYE ])[:,1])
                        self.eye_area = (right_eye_area+left_eye_area)/2
                        self.ratio = self.blinkRatio(frame, mesh_coords, self.RIGHT_EYE, self.LEFT_EYE)
                        self.brightness_value = self.get_average_brightness(rgb_frame,mesh_coords,frame_height,frame_width) 
                        self.eyestate = 0  # **初始化為未眨眼**

                        #area_record[counter] = eye_area 
                        #current_eye_ratio = (np.median(area_record)-eye_area)/np.median(area_record)
                        if self.camera_active == False :
                            
                            if self.ratio > self.blink_th_2.value(): #close eye
                                self.blink_counter +=1
                                self.colorBackgroundText(frame,  f'Blink', FONT, self.FONT_SIZE, (int(frame_height/2), 100), 2, (0,255,255), pad_x=6, pad_y=6, )
                            
                            else: #open eye
                                if self.blink_counter > self.eye_close_frame :
                                    self.blink_per_minute += 1  # **增加每分鐘眨眼次數**
                                    self.blink_counter =0

                            if (self.eye_area_record/self.eye_area)**0.5 < self.distance_th_2.value():
                                    self.colorBackgroundText(frame,  f'Too close', FONT, self.FONT_SIZE, (int(frame_height/2), 150), 2, (0,255,255), pad_x=6, pad_y=6, )

                                    self.showMainWindow('Too close',line=True)

                            if self.brightness_value <self.bright_th_2.value():
                                    self.colorBackgroundText(frame,  f'Too dim', FONT, self.FONT_SIZE, (int(frame_height/2), 150), 2, (0,255,255), pad_x=6, pad_y=6, )
                        self.colorBackgroundText(frame,  f'Total Blinks: {self.total_blink}', FONT, self.FONT_SIZE/2, (30,150),2)
                        cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.LEFT_EYE ], dtype=np.int32)], True,(0,255,0), 1, cv.LINE_AA)
                        cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.RIGHT_EYE ], dtype=np.int32)], True, (0,255,0), 1, cv.LINE_AA)
                        cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.FACE_OVAL ], dtype=np.int32)], True, (0,0,255), 1, cv.LINE_AA)
                    else:
                        self.record_state = 1 # do not detect people
                    self.fps_pass_time = time.time()-self.start_time
                    fps = self.frame_counter/self.fps_pass_time
                    self.colorBackgroundText(frame,  f'Eye area : {(self.eye_area)}', FONT, self.FONT_SIZE/2, (30,90),1)
                    self.colorBackgroundText(frame,  f'Eye Distance ratio: {round((self.eye_area_record/self.eye_area)**0.5,2)}', FONT, self.FONT_SIZE/2, (30,120),1)
                    self.colorBackgroundText(frame,  f'Eye Ratio: {round(self.ratio,2)}', FONT, self.FONT_SIZE/2, (30,150),1)
                    self.colorBackgroundText(frame,  f'Brightness: {round(self.brightness_value,1)}', FONT, self.FONT_SIZE/2, (30,180),1)
                    self.colorBackgroundText(frame,  f'FPS: {round(fps,1)}', FONT,self.FONT_SIZE/2, (30,60),1)
                    self.colorBackgroundText(frame,  f'blink_per_minute: {self.blink_per_minute}', FONT, self.FONT_SIZE/2, (30,450),1)
                    self.colorBackgroundText(frame,  f'status: {self.status}', FONT, self.FONT_SIZE/2, (30,420),1)
                    self.colorBackgroundText(frame,  f'time.status: {self.time_status}', FONT, self.FONT_SIZE/2, (30,390),1)
                    self.colorBackgroundText(frame,  f'record_state: {self.record_state}', FONT, self.FONT_SIZE/2, (30,360),1) 

                    show = cv.resize(frame,(800,600))
                    show = cv.cvtColor(show, cv.COLOR_BGR2RGB)
                    showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
                    self.camera_site_2.setPixmap(QPixmap.fromImage(showImage))        
            elif(self.exercise_type.currentText() == 'jumping jack'):
                FONTS =cv.FONT_HERSHEY_COMPLEX
                self.record_state = 1
                with self.mp_pose.Pose(
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5,model_complexity=0) as pose:
                    success, image = self.camera.read()
                    image = cv.resize(image, None, fx=0.5, fy=0.5, interpolation=cv.INTER_CUBIC)
                    image.flags.writeable = False
                    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                    results = pose.process(image)
                    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
                    if results.pose_world_landmarks:
                        self.record_state = 0
                        mesh_coords = self.landmarksDetection(image, results, False,True)
                        if (self.get_state_body(results)  == -self.previous_state):
                            self.previous_state = self.get_state_body(results)
                            self.count_hand += 1
                            print(self.count_hand,self.count_jump)

                        self.count = self.count_hand
                        image.flags.writeable = True
                        self.mp_drawing.draw_landmarks(
                            image,
                            results.pose_landmarks,
                            self.mp_pose.POSE_CONNECTIONS)
                    image = cv.flip(image, 1)
                    image = self.colorBackgroundText(image,  f'Total : {int(self.count/2)}', FONTS, 0.7, (30,200),1)        
                    show = cv.resize(image,(800,600))
                    show = cv.cvtColor(show, cv.COLOR_BGR2RGB)
                    showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
                    self.camera_site.setPixmap(QPixmap.fromImage(showImage))
                    self.camera_site_2.setPixmap(QPixmap.fromImage(showImage))

            elif((self.exercise_type.currentText() == 'close eye' and self.status != 'shutting_down') or (self.exercise_type.currentText() == 'None' and self.status != 'shutting_down')):
                with self.map_face_mesh.FaceMesh(min_detection_confidence =0.5, min_tracking_confidence=0.5) as face_mesh:
                    self.frame_counter += 1
                    ret, frame = self.camera.read() 
                    frame_height, frame_width= frame.shape[:2]
                    rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
                    results  = face_mesh.process(rgb_frame)
                    FONT = cv.FONT_HERSHEY_COMPLEX

                    if results.multi_face_landmarks and self.exercise_type.currentText() == 'close eye': 
                        self.record_state = 0
                        mesh_coords = self.landmarksDetection(frame, results, False)
                        right_eye_area = self.PolyArea(np.array([mesh_coords[p] for p in self.RIGHT_EYE ])[:,0],np.array([mesh_coords[p] for p in self.RIGHT_EYE ])[:,1])
                        left_eye_area = self.PolyArea(np.array([mesh_coords[p] for p in self.LEFT_EYE ])[:,0],np.array([mesh_coords[p] for p in self.LEFT_EYE ])[:,1])
                        self.eye_area = (right_eye_area+left_eye_area)/2
                        self.ratio = self.blinkRatio(frame, mesh_coords, self.RIGHT_EYE, self.LEFT_EYE)
                        self.brightness_value = self.get_average_brightness(rgb_frame,mesh_coords,frame_height,frame_width) 

                        if  self.ratio > self.blink_th_2.value(): #close eye
                            #self.eyestate = 1 # 1 = blink
                            self.pass_time += (time.time() - self.previous_time_step)
                            self.previous_time_step =  time.time()
                            self.colorBackgroundText(frame,  f'Close', FONT, self.FONT_SIZE, (int(frame_height/2), 100), 2, (0,255,255), pad_x=6, pad_y=6, )
                        else: #open eye
                            #self.eyestate = 0 # 0 = blink
                            #self.pass_time += 0
                            self.previous_time_step = time.time()    
                        cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.LEFT_EYE ], dtype=np.int32)], True,(0,255,0), 1, cv.LINE_AA)
                        cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.RIGHT_EYE ], dtype=np.int32)], True, (0,255,0), 1, cv.LINE_AA)
                        cv.polylines(frame,  [np.array([mesh_coords[p] for p in self.FACE_OVAL ], dtype=np.int32)], True, (0,0,255), 1, cv.LINE_AA)

                    elif self.exercise_type.currentText() == 'None':  # **None 模式下**
                        self.pass_time += (time.time() - self.previous_time_step)
                        self.previous_time_step = time.time()
                        self.record_state = 0  # 明確設置為休息狀態（0）
                    self.fps_pass_time = time.time()-self.start_time
                    fps = self.frame_counter/self.fps_pass_time
                    self.colorBackgroundText(frame,  f'Eye area : {(self.eye_area)}', FONT, self.FONT_SIZE/2, (30,90),1)
                    self.colorBackgroundText(frame,  f'Eye Distance ratio: {(self.eye_area_record/self.eye_area)**0.5}', FONT, self.FONT_SIZE/3, (30,120),1)
                    self.colorBackgroundText(frame,  f'Eye Ratio: {round(self.ratio,3)}', FONT, self.FONT_SIZE/2, (30,150),1)
                    self.colorBackgroundText(frame,  f'Brightness: {round(self.brightness_value,1)}', FONT, self.FONT_SIZE/2, (30,180),1)
                    self.colorBackgroundText(frame,  f'FPS: {round(fps,1)}', FONT, self.FONT_SIZE/2, (30,60),1)
                    self.colorBackgroundText(frame,  f'status: {self.status}', FONT, self.FONT_SIZE/2, (30,420),1)
                    self.colorBackgroundText(frame,  f'time.status: {self.time_status}', FONT, self.FONT_SIZE/2, (30,390),1)
                    self.colorBackgroundText(frame,  f'record_state: {self.record_state}', FONT, self.FONT_SIZE/2, (30,360),1) 

                    show = cv.resize(frame,(800,600))
                    show = cv.cvtColor(show, cv.COLOR_BGR2RGB)
                    showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
                    self.camera_site.setPixmap(QPixmap.fromImage(showImage))
                    self.camera_site_2.setPixmap(QPixmap.fromImage(showImage))
                
            
            if (self.status == 'start' or self.status== 'rest'): 
                if(self.status == 'start'):
                    # 工作時間邏輯 - 不再依賴人臉偵測
                    self.pass_time += (time.time() - self.previous_time_step)  # 無論是否偵測到人臉都累加時間
                    self.previous_time_step = time.time()
                    remain_time = self.work_time*60 - self.pass_time
                elif(self.status == 'rest'):
                    # 休息時間邏輯保持不變
                    remain_time = self.rest_time*60 - self.pass_time                
                hour = remain_time // 3600
                minute = (remain_time - (hour * 3600)) // 60
                second = (remain_time - (hour * 3600) - (minute * 60))

                # 更新進度條
                if self.status == 'start':
                    progress = int(self.pass_time / (self.work_time * 60) * 100)
                elif self.status == 'rest':
                    progress = int(self.pass_time / (self.rest_time * 60) * 100)
                self.Progress_progressBar.setValue(progress)

                self.lcdNumber_hour.display(str(int(hour)))
                self.lcdNumber_min.display(str(int(minute)))
                self.lcdNumber_sec.display(str(int(second)))
                
                self.count_minute += 1 
                self.count_bright += self.brightness_value
                self.count_blink += self.eyestate
                self.count_distance += (self.eye_area_record/self.eye_area)**0.5
                
                pass_minute = (time.time() - self.init_time) // 60
                print(f"pass_minute: {pass_minute}, previous_minute: {self.previous_minute}, status: {self.status}")
                if (pass_minute > self.previous_minute):
                    if self.Exhausted_count == 1:
                        self.Exhausted_state += 1  # 累加疲勞狀態的分鐘數
                    print(f"Minute: {int(pass_minute)}, Exhausted_state: {self.Exhausted_state}")
              
                    self.previous_minute = pass_minute
                    print(f"Minute updated: previous_minute = {self.previous_minute}")

                    # 在計算是否要彈出詢問視窗的地方
                    if self.Exhausted_state >= self.next_threshold and self.status != 'rest':
                        message = "You have been in exhausted state for over {} minutes. Do you want to rest?".format(self.next_threshold)
                        self.showConfirmationDialog(message, self.next_rest_decision)

                    blink_avg = self.blink_per_minute
                    self.blink_per_minute = 0
                    bright_avg = int(self.count_bright/self.count_minute)
                    distance_avg = round(self.count_distance/self.count_minute,3)

                    # **重置計數器**
                    self.count_bright = 0
                    self.count_blink = 0
                    self.count_distance = 0
                    self.count_minute = 0

                    result = time.localtime(time.time())
                    # 取得當前時間
                    current_hour = int(result.tm_hour)  
                    current_minute = int(result.tm_min)
                    #self.current_user  = str(self.nameBox_2.currentText())
                    # 如果分鐘數是 0，則將其設置為 59，並減少小時數
                    if current_minute == 0:
                        current_minute = 59
                        current_hour -= 1
                        # 如果小時數變成負數，則調整為前一天的最後一小時（這應該根據具體需求來處理）
                        if current_hour < 0:
                            current_hour = 23 
                            # 可以在這裡減少天數、月份或年份，根據具體需求來更新時間
                    if self.status == 'start':
                        print(f"Inserting into database: {self.status}, {current_hour}:{current_minute - 1}")
                        self.cursorObj.execute(
                            f"INSERT INTO {self.current_user}_data (year, month, day, hour, minute, distance, brightness, blink, state, Exhausted_state, start_time_for_database) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (int(result.tm_year), int(result.tm_mon), int(result.tm_mday), current_hour, current_minute - 1, distance_avg, bright_avg, blink_avg, self.record_state, self.Exhausted_state, self.start_time_for_database)
                        )
                    elif self.status == 'rest':
                        print(f"Inserting into database: {self.status}, {current_hour}:{current_minute - 1}")
                        self.cursorObj.execute(
                            f"INSERT INTO {self.current_user}_data (year, month, day, hour, minute, distance, brightness, blink, state, Exhausted_state, start_time_for_database) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (int(result.tm_year), int(result.tm_mon), int(result.tm_mday), current_hour, current_minute - 1, 1, 10, 0, self.record_state, self.Exhausted_state, self.start_time_for_database)
                        )

                    self.con.commit()
                    # 插入數據後立即重置`Exhausted_state`
                    #self.Exhausted_state = 0
                    
                    if (self.status == 'start' and self.record_state == 2):  # 確保只有在工作狀態下才檢查眨眼次數
                   # **檢查每分鐘的眨眼次數是否達標**
                        print(f"Current blink_per_minute: {blink_avg}, Threshold: {self.blink_num_th_2.value()}")
                        if blink_avg < self.blink_num_th_2.value():
                            message = f'Low blink rate: {blink_avg} blinks/minute'
                            self.lineNotifyMessage(message)  # 確保只傳送一次
                           
                            self.showMainWindow(message,line=False)
                    print(f"Before reset - blink_per_minute: {blink_avg}, Threshold: {self.blink_num_th_2.value()}")
                    # **重置每分鐘的計數器**
                    self.blink_per_minute = 0                
            
                if (remain_time< 0 and self.status=='start'):
                    print('rest')
                    self.status = 'rest'
                    self.pass_time = 0.01
                    self.previous_time_step = time.time()
                    self.blink_counter = 0
                    message = 'rest now'
                    self.showMainWindow(message,line=False)
                    # 發送LINE提醒，不依賴視窗點擊                        
                    self.lineNotifyMessage(message)                      
                elif((remain_time< 0  or self.count >= self.excerise_count.value()) and self.status=='rest'):
                    message = 'finish rest'
                    self.showMainWindow(message,line=False)
                    # 發送LINE提醒，不依賴視窗點擊                        
                    self.lineNotifyMessage(message)                      
                    self.count = 0
                    self.count_hand = 0
                    self.status = 'start'
                    self.pass_time = 0.01
                    self.previous_time_step = time.time()
                    self.blink_counter = 0
                    self.finish_push_onchange()


        except Exception as e: 
            print(e)
            pass
    
    def sendout(self):
        try:
            # 獲取當下的時間
            current_time = datetime.now()

            # 確保該使用者的 posttest 表存在
            self.cursorObj.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.current_user}_posttest (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_1 TEXT,
                    question_2 TEXT,
                    question_3 TEXT,
                    question_4 TEXT,
                    question_5 TEXT,
                    question_6 TEXT,        
                    question_7 INTEGER,
                    question_8 INTEGER,
                    question_9 INTEGER,
                    question_10 INTEGER,
                    question_11 INTEGER,
                    question_12 TEXT,
                    submission_time TEXT,  -- 填表的時間
                    start_time_for_database TEXT             
                );
            ''')
            self.con.commit()

            # 查詢最近一次的提交時間
            self.cursorObj.execute(f'SELECT submission_time FROM {self.current_user}_posttest ORDER BY id DESC LIMIT 1')
            last_submission = self.cursorObj.fetchone()

            if last_submission:
                # 將 submission_time 字串轉換為 datetime 格式
                last_submission_time = datetime.strptime(last_submission[0], '%Y-%m-%d %H:%M:%S')
                
                # 計算距離上次提交的時間差
                time_difference = current_time - last_submission_time

                if time_difference < timedelta(minutes=2):
                    # 如果時間差小於2分鐘，顯示提示訊息並返回
                    msg_box = QtWidgets.QMessageBox(self)
                    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
                    msg_box.setText(f"請稍候 {int(2 - time_difference.total_seconds() // 60)} 分鐘再提交")
                    msg_box.setWindowTitle("過於頻繁的提交")
                    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msg_box.exec_()
                    return  # 結束函數，避免提交

            # 繼續執行資料插入
            question_1_choice = self.question_1_comboBox.currentText()
            question_2_choice = self.question_2_comboBox.currentText()
            question_3_choice = self.question_3_comboBox.currentText()
            question_4_choice = self.question_4_comboBox.currentText()
            question_5_choice = '是' if self.question_5yes_Button.isChecked() else '否'
            question_6_choice = '是' if self.question_6yes_Button.isChecked() else '否'
            question_7_value = self.question_button_group7.id(self.question_button_group7.checkedButton()) if self.question_button_group7.checkedButton() else None
            question_8_value = self.question_button_group8.id(self.question_button_group8.checkedButton()) if self.question_button_group8.checkedButton() else None
            question_9_value = self.question_button_group9.id(self.question_button_group9.checkedButton()) if self.question_button_group9.checkedButton() else None
            question_10_value = self.question_button_group10.id(self.question_button_group10.checkedButton()) if self.question_button_group10.checkedButton() else None
            question_11_value = self.question_button_group11.id(self.question_button_group11.checkedButton()) if self.question_button_group11.checkedButton() else None
            question_12_text = self.question_12_input.text()
            submission_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

            self.cursorObj.execute(f'''
                INSERT INTO user_id (
                    user_name,test_id
                )VALUES(?,?)
            ''',(
                self.current_user,self.start_time_for_database
                ))
            # 插入新資料到資料庫
            self.cursorObj.execute(f'''
                INSERT INTO {self.current_user}_posttest (
                    question_1, question_2, question_3, question_4, 
                    question_5, question_6, question_7, question_8, 
                    question_9, question_10, question_11, question_12, submission_time, start_time_for_database
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
            ''', (
                question_1_choice, question_2_choice, question_3_choice, question_4_choice,
                question_5_choice, question_6_choice, question_7_value, question_8_value,
                question_9_value, question_10_value, question_11_value, question_12_text, submission_time,self.start_time_for_database
            ))
            self.con.commit()

            print(f"資料已存入 {self.current_user}_posttest，提交時間為 {submission_time}，start_time_for_database為{self.start_time_for_database}")

            # 顯示成功訊息
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setIcon(QtWidgets.QMessageBox.Information)
            msg_box.setText("已送出")
            msg_box.setWindowTitle("確認")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg_box.buttonClicked.connect(lambda: self.switch_page(0))
            msg_box.exec_()
            self.summary_report()

        except sqlite3.Error as e:
            print(f"資料庫操作失敗: {e}")
        except Exception as e:
            print(f"發生錯誤: {e}")


        self.blink_th_2.setValue(self.blink_th.value())
    def clean_up_photos_folder(self):
        """刪除 photos/normal 資料夾內容"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_folder = os.path.join(current_dir, "photos")
        try:
            if os.path.exists(self.image_folder):
                shutil.rmtree(self.image_folder)  # 刪除資料夾及內容
                print(f"🗑️ 已刪除資料夾及內容: {self.image_folder}")
            else:
                print(f"📁 資料夾不存在: {self.image_folder}")
        except Exception as e:
            print(f"❗ 清理資料夾失敗: {self.image_folder}, 錯誤: {e}")   
    def __del__(self):
        self.update_database()
        #self.summary_report()
        self.con.close()
    
    def closeEvent(self, event):
        #self.summary_report()
        self.clean_up_photos_folder()
        self.con.close()


def process_data(db_file,username):  #資料預處理
    if getattr(sys, 'frozen', False):  # 判斷是否為打包後的執行檔
        current_dir = os.path.dirname(sys.executable)  # 執行檔所在目錄
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))

    # 連接主資料庫
    db_file = os.path.join(current_dir, 'database.db')
    conn = sqlite3.connect(db_file)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    table_dataframes = {table_name: pd.read_sql_query(f"SELECT * FROM {table_name}", conn) 
                        for table_name in table_names}

    # Process user_id table
    user_id = table_dataframes['user_id']
    user_id['test_id'] = pd.to_datetime(user_id['test_id'], format='%Y-%m-%d %H:%M:%S')
    user_id['start_time_for_database'] = user_id['test_id'].dt.strftime('%Y%m%d%H%M')
    user_id = user_id[user_id['user_name'] == username]
    user_id = user_id.rename(columns={"user_name": "username"})
    user_id = user_id.drop(['test_id'], axis=1, errors='ignore')

    # Process threshold table
    threshold = table_dataframes['threshold']
    threshold['datetime'] = pd.to_datetime(threshold['insert_time'])
    base_time = datetime(2024, 10, 1, 0, 0, 0)
    threshold['time'] = ((threshold['datetime'] - base_time).dt.total_seconds() / 60).round(0)
    threshold = threshold.rename(columns={"user": "username"})
    threshold = threshold.drop(['id', 'line_token', 'distance_area', 'insert_time', 'datetime'], 
                               axis=1, errors='ignore').dropna()
    threshold = threshold[threshold['username'] != 'None']

    # Process user_info table
    user_info = table_dataframes['user_info']
    user_info = user_info[user_info['username'] == username]
    user_info['start_time_for_database'] = pd.to_datetime(user_info['start_time_for_database'], errors='coerce')
    user_info['start_time_for_database'] = user_info['start_time_for_database'].dt.strftime('%Y%m%d%H%M')
    user_info = user_info.drop(['id', 'start_time_for_database'], axis=1, errors='ignore')

    # Process user_data table
    user_data = table_dataframes[f'{username}_data']
    user_data['start_time_for_database'] = pd.to_datetime(user_data['start_time_for_database'], errors='coerce')
    user_data['start_time_for_database'] = user_data['start_time_for_database'].dt.strftime('%Y%m%d%H%M')
    user_data['datetime'] = pd.to_datetime(user_data[['year', 'month', 'day', 'hour', 'minute']])
    user_data['time'] = (user_data['datetime'] - base_time).dt.total_seconds() / 60
    user_data["username"] = username
    user_data = user_data.drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1, errors='ignore')

    # Process user_posttest table
    user_posttest = table_dataframes[f'{username}_posttest']
    user_posttest['start_time_for_database'] = pd.to_datetime(user_posttest['start_time_for_database'], errors='coerce')
    user_posttest['start_time_for_database'] = user_posttest['start_time_for_database'].dt.strftime('%Y%m%d%H%M')
    user_posttest["username"] = username
    user_posttest = user_posttest.drop(['id', 'question_12', 'submission_time'], axis=1, errors='ignore')

    # Merge tables
    merged_df = pd.merge(user_id, user_info, on=['username'], how='left')
    merged_df = pd.merge(merged_df, user_data, on=['username', 'start_time_for_database'], how='left')
    
    # 檢查和處理 time 列中的 NaN 值
    if merged_df['time'].isnull().sum() > 0:
        print(f"merged_df 中有 {merged_df['time'].isnull().sum()} 個 NaN 值")
        merged_df['time'] = merged_df['time'].fillna(0)  # 或使用 dropna()

    if threshold['time'].isnull().sum() > 0:
        print(f"threshold 中有 {threshold['time'].isnull().sum()} 個 NaN 值")
        threshold['time'] = threshold['time'].fillna(0)  # 或使用 dropna()

    
    print(merged_df)
    print(threshold)
    merged_df = pd.merge_asof(merged_df.sort_values('time'), threshold.sort_values('time'), 
                              on='time', by='username', direction='backward')
    merged_df = pd.merge(merged_df, user_posttest, on=['username', 'start_time_for_database'], how='left')

    # Save to CSV
    #output_file = f"{username}_cleandata.csv"
    #merged_df.to_csv(output_file, index=False, encoding='utf-8')
    print("合併完成")

    '''USER_ID'''
    merged_df['USER_ID_HASH'] = merged_df.apply(
        lambda row: int(hashlib.sha256(f"{row['username']}{row['start_time_for_database']}".encode()).hexdigest(), 16),
        axis=1
    )

    '''Label Encoding'''
    merged_df['gender'] = merged_df['gender'].map({'男生': 1, '女生': 2})
    merged_df['right_eye_shine'] = merged_df['right_eye_shine'].map({'有': 1, '無': 0})
    merged_df['left_eye_shine'] = merged_df['left_eye_shine'].map({'有': 1, '無': 0})
    merged_df['use_situation1'] = merged_df['use_situation1'].map({'是': 1, '否': 0})
    merged_df['use_situation3'] = merged_df['use_situation3'].map({'是': 1, '否': 0})
    merged_df['habit1'] = merged_df['habit1'].map({'是': 1, '否': 0})
    merged_df['habit2'] = merged_df['habit2'].map({'有': 1, '無': 0})
    merged_df['question_5'] = merged_df['question_5'].map({'是': 1, '否': 0})
    merged_df['question_6'] = merged_df['question_6'].map({'是': 1, '否': 0})
    print("Label Encoding完成")

    '''二進制編碼'''
    binary_map = {"無": "00","近視": "01","遠視": "10"}
    merged_df['right_eye_condition'] = merged_df['right_eye_condition'].map(binary_map)
    merged_df['left_eye_condition'] = merged_df['left_eye_condition'].map(binary_map)
    print("二進制編碼完成")

    '''One-Hot Encoding'''
    possible_columns = {
        "use_situation2": ["3小時以內","3至6小時","6-9小時",
                        "9-12小時","12小時以上" ],
        "use_situation_value4": ["電腦自動調整",
                                "不常調整",
                                "每次使用都會調整"
                                ],
        "use_situation_value5": ["僅室內共用燈光",
                                "僅室內專用燈光",
                                "室內共用與專用燈光皆有",
                                "戶外",
                                "光線明顯不足之環境",
                                "其他" ],
        "habit2": ["無","半年一次","一年一次","更頻繁"],
        "habit3": ["低於4小時","4至6小時","6至8小時","高於8小時"],
        "habit4": ["0或1次","2或3次","4或5次","6次以上"],
        "habit5": ['無休息',"1小時內","1-2小時","2-3小時",
                "3-4小時","4-5小時", "5小時以上"],
        "habit6": ["10分鐘內","11-30分鐘","31-60分鐘","60分鐘以上"],
        "habit7": ["眼部運動",'閉目養神','其他',
                '閉目養神, 眼部運動','閉目養神, 其他','眼部運動, 其他',
                '閉目養神, 眼部運動, 其他'],
        "question_1": ["電腦", "手機", "平板","其他"],
        "question_2": ["工作/實習用途", "聆聽線上課程","完成學校作業", "打電腦遊戲",
                    "觀看影音串流平台(如youtube)","回復訊息文字","其他"],
        "question_3": ["僅室內共用燈光","僅室內專用燈光", "戶外", "光線明顯不足之環境","其他" ],
        "question_4": ["無", "配戴眼鏡", "配戴隱形眼鏡"]
    }

    # 創建副本以避免直接修改原始數據
    processed_data = merged_df.copy()

    # 替換欄位
    for col, possible_values in possible_columns.items():
        # 獲取當前數據的獨熱編碼
        one_hot = pd.get_dummies(merged_df[col], prefix=col)
        
        # 添加缺失的類別列（以 0 填充）
        for value in possible_values:
            col_name = f"{col}_{value}"
            if col_name not in one_hot.columns:
                one_hot[col_name] = 0
        
        # 按照可能值的順序排列列
        one_hot = one_hot[[f"{col}_{value}" for value in possible_values]]
        
        # 刪除原始欄位並將新編碼欄位插入
        processed_data = processed_data.drop(columns=[col]).reset_index(drop=True)
        processed_data = pd.concat([processed_data, one_hot], axis=1)
    print("One-Hot Encoding完成")

    ''' 計算年齡 '''
    processed_data["birthday"] = processed_data["birthday"].apply(
        lambda birthday: datetime.today().year - datetime.strptime(str(birthday), "%Y%m%d").year - 
        ((datetime.today().month, datetime.today().day) < 
        (datetime.strptime(str(birthday), "%Y%m%d").month, datetime.strptime(str(birthday), "%Y%m%d").day))
    )
    processed_data = processed_data.rename(columns={"birthday": "age"})
    print("計算年齡 完成")

    processed_data = processed_data.drop(['username', 'name','start_time_for_database','line_token'], axis=1, errors='ignore')
    print("drop完成")


    print("轉換前數據預覽:")
    print(processed_data.head())

    # 替換空字符串為 NaN
    processed_data = processed_data.replace('', np.nan)

    # 確保每列都可以安全轉換為浮點數
    for col in processed_data.columns:
        try:
         processed_data[col] = pd.to_numeric(processed_data[col], errors='coerce')
        except Exception as e:
            print(f"列 {col} 轉換失敗: {e}")

    # 再次檢查數據
    print("轉換後數據預覽:")
    print(processed_data.head())

    # 將目標欄位移動到最前面
    column_to_move = "USER_ID_HASH"
    processed_data = processed_data[[column_to_move] + [col for col in processed_data.columns if col != column_to_move]]  
    print("移動完成")  
    #print(processed_data) 
    #processed_data.to_csv('D:\SCU\eyemyself\eye_1127\processed_data.csv',index=False, encoding='utf-8-sig')

                                    
    processed_data = processed_data.astype(float)
    print("編碼完成")

    # === Step 2: 新增轉變標籤 ===
    processed_data['Transition'] = processed_data.groupby('USER_ID_HASH')['Exhausted_state'].transform(
        lambda x: (x.shift() == 0) & (x == 1)
    ).astype(int)


    # === Step 3: 計算首次轉變時間差 ===
    def calculate_time_diff(df):
        start_time = df['time'].iloc[0]
        if df['Transition'].sum() > 0:  # 如果有轉變
            transition_time = df.loc[df['Transition'] == 1, 'time'].iloc[0]
            df['time_diff_to_first_exhausted'] = transition_time - start_time
        else:
            df['time_diff_to_first_exhausted'] = 0 
        return df

    data = processed_data.groupby('USER_ID_HASH', group_keys=False, as_index=False).apply(calculate_time_diff)

    # === Step 4: 計算移動特徵 ===
    def add_moving_features(df):
        df['distance_moving_avg'] = df.groupby('USER_ID_HASH')['distance'].transform(
            lambda x: x.rolling(window=5, min_periods=1).mean()
        )
        df['cumulative_distance'] = df.groupby('USER_ID_HASH')['distance'].cumsum()
        df['cumulative_time'] = df.groupby('USER_ID_HASH')['time'].transform(lambda x: x - x.min())
        return df

    data = add_moving_features(data)

    # === Step 5: 過濾資料 ===
    def filter_first_transition(df):
        if df['Transition'].sum() == 0:  # 若無轉變，保留所有資料
            return df
        first_transition_index = df[df['Transition'] == 1].index[0]
        return df[df.index <= first_transition_index]

    filtered_data = data.groupby('USER_ID_HASH', group_keys=False).apply(filter_first_transition).reset_index(drop=True)

    # 計算相關矩陣
    correlation_matrix = filtered_data.corr()
    correlation_with_target = correlation_matrix['time_diff_to_first_exhausted'].drop('time_diff_to_first_exhausted')
    print("與 time_diff_to_first_exhausted 的相關係數：")
    print(correlation_with_target)

    highly_correlated_features = correlation_with_target[
        ((correlation_with_target >= 0.5) | (correlation_with_target <= -0.5)) &
        (correlation_with_target.index != 'USER_ID_HASH')
    ].index.tolist()

    features_to_impute = ['time_diff_to_first_exhausted'] + [feature for feature in highly_correlated_features if feature != 'time_diff_to_first_exhausted']

    print("用於填補的特徵：", features_to_impute)
    print(f"filtered_data 有 {len(filtered_data.columns)} 個欄位")

    # 用 KNNImputer 填補缺失值
    imputer = KNNImputer(n_neighbors=5)  # 建立 KNNImputer 模型
    filtered_data[features_to_impute] = imputer.fit_transform(filtered_data[features_to_impute])  # 填補缺失值

    # === Step 6: 特徵選擇與清理 ===
    feature_cols = ['USER_ID_HASH',
    'age','gender',
    'right_eye_condition','right_eye_degree','right_eye_shine','right_eye_shine_degree',
    'left_eye_condition','left_eye_degree','left_eye_shine','left_eye_shine_degree',
    'eye_situation_value1','eye_situation_value2','eye_situation_value3','eye_situation_value4','eye_situation_value5',
    'use_situation1','use_situation3','habit1',
    'distance','brightness_x','blink_x','state','Exhausted_state','time',
    'distance_ratio','brightness_y','blink_y','blink_num',
    'question_5','question_6','question_7','question_8','question_9','question_10','question_11',
    'use_situation2_3小時以內','use_situation2_3至6小時','use_situation2_6-9小時','use_situation2_9-12小時','use_situation2_12小時以上',
    'use_situation_value4_電腦自動調整','use_situation_value4_不常調整','use_situation_value4_每次使用都會調整',
    'use_situation_value5_僅室內共用燈光','use_situation_value5_僅室內專用燈光','use_situation_value5_室內共用與專用燈光皆有','use_situation_value5_戶外','use_situation_value5_光線明顯不足之環境','use_situation_value5_其他',
    'habit2_無','habit2_半年一次','habit2_一年一次','habit2_更頻繁',
    'habit3_低於4小時','habit3_4至6小時','habit3_6至8小時','habit3_高於8小時',
    'habit4_0或1次','habit4_2或3次','habit4_4或5次','habit4_6次以上',
    'habit5_無休息','habit5_1小時內','habit5_1-2小時','habit5_2-3小時','habit5_3-4小時','habit5_4-5小時','habit5_5小時以上',
    'habit6_10分鐘內','habit6_11-30分鐘','habit6_31-60分鐘','habit6_60分鐘以上',
    'habit7_眼部運動','habit7_閉目養神','habit7_其他','habit7_閉目養神, 眼部運動','habit7_閉目養神, 其他','habit7_眼部運動, 其他','habit7_閉目養神, 眼部運動, 其他',
    'question_1_電腦','question_1_手機','question_1_平板','question_1_其他',
    'question_2_工作/實習用途','question_2_聆聽線上課程', 'question_2_完成學校作業','question_2_打電腦遊戲','question_2_觀看影音串流平台(如youtube)','question_2_回復訊息文字','question_2_其他',
    'question_3_僅室內共用燈光','question_3_僅室內專用燈光','question_3_戶外','question_3_光線明顯不足之環境','question_3_其他',
    'question_4_無','question_4_配戴眼鏡','question_4_配戴隱形眼鏡',
    'Transition','time_diff_to_first_exhausted','distance_moving_avg','cumulative_distance','cumulative_time']

    filtered_data = filtered_data.dropna(subset=feature_cols)  # 移除缺失值
    print('特徵值處理完成')

    # 輸出為新的 CSV 文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, f"{username}_final_data.csv")
    filtered_data.to_csv(output_file, index=False, encoding='utf-8-sig')    
    return output_file



def get_json_file_path(file_name): 
    """取得 JSON 檔案的正確路徑"""
    if getattr(sys, 'frozen', False):  # 如果是打包後的執行檔
        base_path = sys._MEIPASS  # PyInstaller 解壓縮的臨時目錄
    else:  # 開發環境
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, file_name)


def upload_to_google_drive(file_path): #上傳google drive
    """
    上傳單一檔案到 Google Drive。
    
    Parameters:
        file_path (str): 要上傳的檔案完整路徑。
    """
    try:
        # 使用服務帳戶的 JSON 憑證檔案路徑
        SERVICE_ACCOUNT_FILE = get_json_file_path('eye-myself-357cdddd6407.json')
        SCOPES = ['https://www.googleapis.com/auth/drive.file']

        # 初始化 Google API 憑證
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # 建立 Google Drive API 服務
        service = build('drive', 'v3', credentials=credentials)

        # 指定目標資料夾的 ID
        folder_id = '1rowZJjh184Ogz5STLAGwms5utm2z8lsn'

        # 確認檔案是否存在
        if not os.path.exists(file_path):
            print(f"檔案不存在，無法上傳：{file_path}")
            return

        # 檔案名稱
        file_name = os.path.basename(file_path)

        # 檢查是否已有同名文件
        query = f"'{folder_id}' in parents and name = '{file_name}' and trashed=false"
        response = service.files().list(q=query, spaces='drive').execute()
        files = response.get('files', [])

        # 如果有同名文件，刪除它
        if files:
            file_id = files[0]['id']
            service.files().delete(fileId=file_id).execute()
            print(f"Deleted existing file: {file_name} (ID: {file_id})")

        # 定義檔案的元數據，包括父資料夾 ID
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        # 讀取並上傳檔案
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"'{file_name}' 已成功上傳到 Google Drive 中的「畢業專題」資料夾。")

    except Exception as e:
        print(f"Failed to upload file to Google Drive: {e}")



if __name__ == '__main__':
    app = QApplication([])
    # apply_stylesheet(app, theme='dark_blue.xml')
    window = Window()
    window.show()
    app.exec()

    # 在此處執行數據處理邏輯
    if window.current_user:  # 確認有選中的使用者
        try:
            # 取得資料庫路徑
            db_path = window.db_path
            print(f"開始處理資料，使用者: {window.current_user}")
            
            # 呼叫 process_data 處理數據
            processed_file = process_data(window.db_path, window.current_user)
            print(f"數據處理完成，輸出檔案: {processed_file}")
            #upload_to_google_drive(processed_file)
        except Exception as e:
            print(f"數據處理失敗: {e}")
