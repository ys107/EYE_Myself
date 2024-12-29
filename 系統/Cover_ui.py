from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1108, 670)
        MainWindow.setAutoFillBackground(False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1101, 641))
        self.stackedWidget.setObjectName("stackedWidget")

        self.page_1 = QtWidgets.QWidget()
        self.page_1.setAutoFillBackground(False)
        self.page_1.setObjectName("page_1")
        
        # 創建一個 QLabel 用於顯示圖片
        self.firstpage_picture_label = QtWidgets.QLabel(self.page_1)
        self.firstpage_picture_label.setGeometry(0, 0, 1108, 670)  # 直接設置尺寸
        self.firstpage_picture_label.setScaledContents(True)  # 讓圖片自動縮放
        #self.firstpage_picture_label.setPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\firstpage_2.png").scaled(1108, 670, QtCore.Qt.IgnoreAspectRatio))
        self.firstpage_picture_label.setAlignment(QtCore.Qt.AlignCenter)

        self.login = QtWidgets.QToolButton(self.page_1)
        self.login.setGeometry(QtCore.QRect(433, 448, 234, 53))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.login.setFont(font)
        self.login.setAutoRaise(False)
        self.login.setStyleSheet("""
                                    background-color: transparent; 
                                    color: transparent; 
                                    border: none;
                                """)        
        self.login.setObjectName("login")

        self.Signup = QtWidgets.QPushButton(self.page_1)
        self.Signup.setGeometry(QtCore.QRect(715, 100, 70, 85))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Signup.setFont(font)
        self.Signup.setStyleSheet("""
                                    QPushButton {
                                        background-color: transparent; 
                                        color: transparent; 
                                        border: none;
                                    }
                                    QPushButton:hover {
                                        color: #32466A;  /* 當鼠標懸停時顯示文字 */
                                        padding-top: 65px;    /* 向下偏移文字位置 */
                                        text-align: center;    /* 文字對齊方式，可選 left, right, center */
                                    }
                                """)
        self.Signup.setObjectName("Signup")
        
        
        
        
        
        

        self.Edit = QtWidgets.QPushButton(self.page_1)
        self.Edit.setGeometry(QtCore.QRect(788, 105, 70, 85))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Edit.setFont(font)
        self.Edit.setStyleSheet("""
                                    QPushButton {
                                        background-color: transparent; 
                                        color: transparent; 
                                        border: none;
                                    }
                                    QPushButton:hover {
                                        color: #32466A;  /* 當鼠標懸停時顯示文字 */
                                        padding-top: 60px;    /* 向下偏移文字位置 */
                                        text-align: center;    /* 文字對齊方式，可選 left, right, center */
                                    }
                                """)
        self.Edit.setObjectName("Edit")

        self.Analysis = QtWidgets.QPushButton(self.page_1)
        self.Analysis.setGeometry(QtCore.QRect(861, 105, 70, 85))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Analysis.setFont(font)
        self.Analysis.setStyleSheet("""
                                    QPushButton {
                                        background-color: transparent; 
                                        color: transparent; 
                                        border: none;
                                    }
                                    QPushButton:hover {
                                        color: #32466A;  /* 當鼠標懸停時顯示文字 */
                                        padding-top: 60px;    /* 向下偏移文字位置 */
                                        text-align: center;    /* 文字對齊方式，可選 left, right, center */
                                    }
                                """)        
        self.Analysis.setObjectName("Analysis")

        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")

        # 創建一個 QLabel 用於顯示圖片
        self.secondpage_picture_label_2 = QtWidgets.QLabel(self.page_2)
        self.secondpage_picture_label_2.setGeometry(0, 0, 1108, 670)  # 直接設置尺寸
        self.secondpage_picture_label_2.setScaledContents(True)  # 讓圖片自動縮放
        #self.secondpage_picture_label_2.setPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\底圖_4.png").scaled(1108, 670, QtCore.Qt.IgnoreAspectRatio))
        self.secondpage_picture_label_2.setAlignment(QtCore.Qt.AlignCenter)

        self.camera_site = QtWidgets.QLabel(self.page_2)
        self.camera_site.setGeometry(QtCore.QRect(30, 40, 701, 581))
        self.camera_site.setText("")
        self.camera_site.setObjectName("camera_site")

        self.name_label = QtWidgets.QLabel(self.page_2)
        self.name_label.setGeometry(QtCore.QRect(790, 60, 58, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")

        self.open_camera = QtWidgets.QPushButton(self.page_2)
        self.open_camera.setGeometry(QtCore.QRect(870, 110, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.open_camera.setFont(font)
        self.open_camera.setObjectName("open_camera")


        #blink
        self.label_2 = QtWidgets.QLabel(self.page_2)
        self.label_2.setGeometry(QtCore.QRect(790, 190, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.blink_th = QtWidgets.QDoubleSpinBox(self.page_2)
        self.blink_th.setEnabled(True)
        self.blink_th.setGeometry(QtCore.QRect(980, 190, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blink_th.sizePolicy().hasHeightForWidth())
        self.blink_th.setSizePolicy(sizePolicy)
        self.blink_th.setDecimals(1)
        self.blink_th.setMinimum(0.0)
        self.blink_th.setMaximum(10.0)
        self.blink_th.setSingleStep(0.1)
        self.blink_th.setProperty("value", 4.0)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.blink_th.setFont(font)
        self.blink_th.setObjectName("blink_th")

        #brightness
        self.label_3 = QtWidgets.QLabel(self.page_2)
        self.label_3.setGeometry(QtCore.QRect(790, 230, 185, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.bright_th = QtWidgets.QDoubleSpinBox(self.page_2)
        self.bright_th.setEnabled(True)
        self.bright_th.setGeometry(QtCore.QRect(980, 230, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bright_th.sizePolicy().hasHeightForWidth())
        self.bright_th.setSizePolicy(sizePolicy)
        self.bright_th.setMinimum(0)
        self.bright_th.setMaximum(1000)
        self.bright_th.setSingleStep(1)
        self.bright_th.setProperty("value", 80.0)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.bright_th.setFont(font)
        self.bright_th.setObjectName("bright_th")

        #distance
        self.label_4 = QtWidgets.QLabel(self.page_2)
        self.label_4.setGeometry(QtCore.QRect(790, 270, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.distance_th = QtWidgets.QDoubleSpinBox(self.page_2)
        self.distance_th.setEnabled(True)
        self.distance_th.setGeometry(QtCore.QRect(980, 270, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.distance_th.sizePolicy().hasHeightForWidth())
        self.distance_th.setSizePolicy(sizePolicy)
        self.distance_th.setDecimals(2)
        self.distance_th.setMinimum(0.0)
        self.distance_th.setMaximum(2.0)
        self.distance_th.setSingleStep(0.01)
        self.distance_th.setProperty("value", 0.88)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.distance_th.setFont(font)
        self.distance_th.setObjectName("distance_th")

        #眨眼數字
        self.blink_num = QtWidgets.QLabel(self.page_2)
        self.blink_num.setGeometry(QtCore.QRect(790, 310, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.blink_num.setFont(font)
        self.blink_num.setObjectName("blink_num")

        self.blink_num_th = QtWidgets.QSpinBox(self.page_2)
        self.blink_num_th.setEnabled(True)
        self.blink_num_th.setGeometry(QtCore.QRect(980, 310, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blink_num_th.sizePolicy().hasHeightForWidth())
        self.blink_num_th.setSizePolicy(sizePolicy)
        self.blink_num_th.setMinimum(0)
        self.blink_num_th.setMaximum(120)
        self.blink_num_th.setSingleStep(1)
        self.blink_num_th.setProperty("value", 15)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.blink_num_th.setFont(font)
        self.blink_num_th.setObjectName("blink_num_th")

        #working
        self.label_5 = QtWidgets.QLabel(self.page_2)
        self.label_5.setGeometry(QtCore.QRect(790, 375, 121, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.working_time = QtWidgets.QSpinBox(self.page_2)
        self.working_time.setEnabled(True)
        self.working_time.setGeometry(QtCore.QRect(980, 375, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.working_time.sizePolicy().hasHeightForWidth())
        self.working_time.setSizePolicy(sizePolicy)
        self.working_time.setMinimum(0)
        self.working_time.setMaximum(60)
        self.working_time.setSingleStep(1)
        self.working_time.setProperty("value", 25)
        font = QtGui.QFont()
        font.setFamily("Arial")
        #font.setPointSize(14)
        self.working_time.setFont(font)
        self.working_time.setObjectName("working_time")

        #min
        self.label_6 = QtWidgets.QLabel(self.page_2)
        self.label_6.setGeometry(QtCore.QRect(1050, 375, 31, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        #rest
        self.label_7 = QtWidgets.QLabel(self.page_2)
        self.label_7.setGeometry(QtCore.QRect(790, 415, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.resting_time = QtWidgets.QSpinBox(self.page_2)
        self.resting_time.setEnabled(True)
        self.resting_time.setGeometry(QtCore.QRect(980, 415, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resting_time.sizePolicy().hasHeightForWidth())
        self.resting_time.setSizePolicy(sizePolicy)
        self.resting_time.setMinimum(0)
        self.resting_time.setMaximum(60)
        self.resting_time.setSingleStep(1)
        self.resting_time.setProperty("value", 5.0)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.resting_time.setFont(font)
        self.resting_time.setObjectName("resting_time")

        #min下
        self.label_8 = QtWidgets.QLabel(self.page_2)
        self.label_8.setGeometry(QtCore.QRect(1050, 415, 31, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")

        #type
        self.label_9 = QtWidgets.QLabel(self.page_2)
        self.label_9.setGeometry(QtCore.QRect(790, 475, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        self.nameBox = QtWidgets.QComboBox(self.page_2)
        self.nameBox.setGeometry(QtCore.QRect(870, 60, 171, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.nameBox.setFont(font)
        self.nameBox.setObjectName("nameBox")

        self.exercise_type = QtWidgets.QComboBox(self.page_2)
        self.exercise_type.setGeometry(QtCore.QRect(925, 475, 121, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exercise_type.sizePolicy().hasHeightForWidth())
        self.exercise_type.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.exercise_type.setFont(font)
        self.exercise_type.setObjectName("exercise_type")

        #number
        self.label_10 = QtWidgets.QLabel(self.page_2)
        self.label_10.setGeometry(QtCore.QRect(790, 515, 111, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")

        self.excerise_count = QtWidgets.QSpinBox(self.page_2)
        self.excerise_count.setEnabled(True)
        self.excerise_count.setGeometry(QtCore.QRect(980, 515, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.excerise_count.sizePolicy().hasHeightForWidth())
        self.excerise_count.setSizePolicy(sizePolicy)
        self.excerise_count.setMinimum(0)
        self.excerise_count.setMaximum(1000)
        self.excerise_count.setSingleStep(1)
        self.excerise_count.setProperty("value", 80.0)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.excerise_count.setFont(font)
        self.excerise_count.setObjectName("excerise_count")

        self.suggestion = QtWidgets.QToolButton(self.page_2)
        self.suggestion.setGeometry(QtCore.QRect(785, 565, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.suggestion.setFont(font)
        self.suggestion.setObjectName("suggestion")

        self.start = QtWidgets.QToolButton(self.page_2)
        self.start.setEnabled(True)
        self.start.setGeometry(QtCore.QRect(940, 565, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.start.setFont(font)
        self.start.setObjectName("start")

        #Log in （點login進去後的頁面 要選擇使用者的頁面）
        self.login1_homebutton = QtWidgets.QPushButton(self.page_2)
        self.login1_homebutton.setGeometry(QtCore.QRect(1060, 10, 31, 31))
        self.login1_homebutton.setText("")
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\home-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.login1_homebutton.setIcon(icon)
        #self.login1_homebutton.setIconSize(QtCore.QSize(30,30))
        self.login1_homebutton.setObjectName("login1_homebutton")
               # 設置樣式，讓按鈕背景透明並移除邊框
        self.login1_homebutton.setStyleSheet("""
            QPushButton {
                background-color: transparent;  /* 背景透明 */
                border: none;                  /* 無邊框 */
            }
        """)
        
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")

        # 創建一個 QLabel 用於顯示圖片
        self.secondpage_picture_label_3 = QtWidgets.QLabel(self.page_3)
        self.secondpage_picture_label_3.setGeometry(0, 0, 1108, 670)  # 直接設置尺寸
        self.secondpage_picture_label_3.setScaledContents(True)  # 讓圖片自動縮放
        #self.secondpage_picture_label_3.setPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\底圖_4.png").scaled(1108, 670, QtCore.Qt.IgnoreAspectRatio))
        self.secondpage_picture_label_3.setAlignment(QtCore.Qt.AlignCenter)

        self.camera_site_2 = QtWidgets.QLabel(self.page_3)
        self.camera_site_2.setGeometry(QtCore.QRect(30, 40, 701, 581))
        self.camera_site_2.setText("")
        self.camera_site_2.setObjectName("camera_site_2")

        self.name_label_2 = QtWidgets.QLabel(self.page_3)
        self.name_label_2.setGeometry(QtCore.QRect(790, 60, 58, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.name_label_2.setFont(font)
        self.name_label_2.setObjectName("name_label_2")

        self.nameBox_2 = QtWidgets.QComboBox(self.page_3)
        self.nameBox_2.setGeometry(QtCore.QRect(870, 60, 171, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.nameBox_2.setFont(font)
        self.nameBox_2.setObjectName("nameBox_2")

        self.label_11 = QtWidgets.QLabel(self.page_3)
        self.label_11.setGeometry(QtCore.QRect(790, 160, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")

        self.label_12 = QtWidgets.QLabel(self.page_3)
        self.label_12.setGeometry(QtCore.QRect(790, 120, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")

        self.label_13 = QtWidgets.QLabel(self.page_3)
        self.label_13.setGeometry(QtCore.QRect(790, 200, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")

        self.blink_th_2 = QtWidgets.QDoubleSpinBox(self.page_3)
        self.blink_th_2.setEnabled(True)
        self.blink_th_2.setGeometry(QtCore.QRect(980, 120, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blink_th_2.sizePolicy().hasHeightForWidth())
        self.blink_th_2.setSizePolicy(sizePolicy)
        self.blink_th_2.setDecimals(1)
        self.blink_th_2.setMinimum(0.0)
        self.blink_th_2.setMaximum(10.0)
        self.blink_th_2.setSingleStep(0.1)
        self.blink_th_2.setProperty("value", 4.0)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.blink_th_2.setFont(font)
        self.blink_th_2.setObjectName("blink_th_2")

        self.bright_th_2 = QtWidgets.QDoubleSpinBox(self.page_3)
        self.bright_th_2.setEnabled(True)
        self.bright_th_2.setGeometry(QtCore.QRect(980, 160, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bright_th_2.sizePolicy().hasHeightForWidth())
        self.bright_th_2.setSizePolicy(sizePolicy)
        self.bright_th_2.setMinimum(0)
        self.bright_th_2.setMaximum(1000)
        self.bright_th_2.setSingleStep(1)
        self.bright_th_2.setProperty("value", 80.0)        
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.bright_th_2.setFont(font)
        self.bright_th_2.setObjectName("bright_th_2")

        self.distance_th_2 = QtWidgets.QDoubleSpinBox(self.page_3)
        self.distance_th_2.setEnabled(True)
        self.distance_th_2.setGeometry(QtCore.QRect(980, 200, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.distance_th_2.sizePolicy().hasHeightForWidth())
        self.distance_th_2.setSizePolicy(sizePolicy)
        self.distance_th_2.setDecimals(2)
        self.distance_th_2.setMinimum(0.0)
        self.distance_th_2.setMaximum(2.0)
        self.distance_th_2.setSingleStep(0.01)
        self.distance_th_2.setProperty("value", 0.88)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.distance_th_2.setFont(font)
        self.distance_th_2.setObjectName("distance_th_2")

        self.blink_num_1 = QtWidgets.QLabel(self.page_3)
        self.blink_num_1.setGeometry(QtCore.QRect(790, 240, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.blink_num_1.setFont(font)
        self.blink_num_1.setObjectName("blink_num_1")

        self.blink_num_th_2 = QtWidgets.QSpinBox(self.page_3)
        self.blink_num_th_2.setEnabled(True)
        self.blink_num_th_2.setGeometry(QtCore.QRect(980, 240, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.blink_num_th_2.sizePolicy().hasHeightForWidth())
        self.blink_num_th_2.setSizePolicy(sizePolicy)
        self.blink_num_th_2.setMinimum(0)
        self.blink_num_th_2.setMaximum(120)
        self.blink_num_th_2.setSingleStep(1)
        self.blink_num_th_2.setValue(self.blink_num_th.value())
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.blink_num_th_2.setFont(font)
        self.blink_num_th_2.setObjectName("blink_num_th_2")

        self.pushButton_sve = QtWidgets.QPushButton(self.page_3)
        self.pushButton_sve.setGeometry(QtCore.QRect(880, 280, 93, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_sve.sizePolicy().hasHeightForWidth())
        self.pushButton_sve.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_sve.setFont(font)
        self.pushButton_sve.setObjectName("pushButton_sve")

        self.line = QtWidgets.QFrame(self.page_3)
        self.line.setGeometry(QtCore.QRect(770, 325, 311, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.lcdNumber_sec = QtWidgets.QLCDNumber(self.page_3)
        self.lcdNumber_sec.setGeometry(QtCore.QRect(980, 355, 64, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumber_sec.sizePolicy().hasHeightForWidth())
        self.lcdNumber_sec.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lcdNumber_sec.setFont(font)
        self.lcdNumber_sec.setDigitCount(2)
        self.lcdNumber_sec.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_sec.setObjectName("lcdNumber_sec")

        self.lcdNumber_min = QtWidgets.QLCDNumber(self.page_3)
        self.lcdNumber_min.setGeometry(QtCore.QRect(880, 355, 64, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumber_min.sizePolicy().hasHeightForWidth())
        self.lcdNumber_min.setSizePolicy(sizePolicy)
        self.lcdNumber_min.setDigitCount(2)
        self.lcdNumber_min.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_min.setObjectName("lcdNumber_min")

        self.lcdNumber_hour = QtWidgets.QLCDNumber(self.page_3)
        self.lcdNumber_hour.setGeometry(QtCore.QRect(770, 355, 64, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumber_hour.sizePolicy().hasHeightForWidth())
        self.lcdNumber_hour.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lcdNumber_hour.setFont(font)
        self.lcdNumber_hour.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lcdNumber_hour.setSmallDecimalPoint(False)
        self.lcdNumber_hour.setDigitCount(2)
        self.lcdNumber_hour.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_hour.setProperty("value", 0.0)
        self.lcdNumber_hour.setObjectName("lcdNumber_hour")

        self.Hour = QtWidgets.QLabel(self.page_3)
        self.Hour.setGeometry(QtCore.QRect(840, 355, 41, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Hour.sizePolicy().hasHeightForWidth())
        self.Hour.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Hour.setFont(font)
        self.Hour.setObjectName("Hour")

        self.Second = QtWidgets.QLabel(self.page_3)
        self.Second.setGeometry(QtCore.QRect(1050, 355, 41, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Second.sizePolicy().hasHeightForWidth())
        self.Second.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Second.setFont(font)
        self.Second.setObjectName("Second")

        self.Minute = QtWidgets.QLabel(self.page_3)
        self.Minute.setGeometry(QtCore.QRect(950, 355, 31, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Minute.sizePolicy().hasHeightForWidth())
        self.Minute.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Minute.setFont(font)
        self.Minute.setObjectName("Minute")

        self.Progress_progressBar = QtWidgets.QProgressBar(self.page_3)
        self.Progress_progressBar.setGeometry(QtCore.QRect(780, 400, 291, 23))
        self.Progress_progressBar.setProperty("value", 0)
        self.Progress_progressBar.setObjectName("Progress_progressBar")

        self.pushButton_Exhausted = QtWidgets.QPushButton(self.page_3)
        self.pushButton_Exhausted.setGeometry(QtCore.QRect(770, 470, 121, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Exhausted.sizePolicy().hasHeightForWidth())
        self.pushButton_sve.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Exhausted.setFont(font)
        self.pushButton_Exhausted.setObjectName("pushButton_Exhausted")

        self.listView = QtWidgets.QListView(self.page_3)
        self.listView.setGeometry(QtCore.QRect(900, 440, 181, 121))
        self.listView.setObjectName("listView")

        self.toolButton_finish = QtWidgets.QToolButton(self.page_3)
        self.toolButton_finish.setGeometry(QtCore.QRect(860, 590, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.toolButton_finish.setFont(font)
        self.toolButton_finish.setObjectName("toolButton_finish")

        #Log in （按了start鍵之後開始測 要跳出一個警示匡說紀錄不保留喔）
        self.login2_homebutton = QtWidgets.QPushButton(self.page_3)
        self.login2_homebutton.setGeometry(QtCore.QRect(1060, 10, 31, 31))
        self.login2_homebutton.setText("")
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\home-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.login2_homebutton.setIcon(icon)
        #self.login2_homebutton.setIconSize(QtCore.QSize(30,30))
        self.login2_homebutton.setObjectName("login2_homebutton")
               # 設置樣式，讓按鈕背景透明並移除邊框
        self.login2_homebutton.setStyleSheet("""
            QPushButton {
                background-color: transparent;  /* 背景透明 */
                border: none;                  /* 無邊框 */
            }
        """)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        
        # 創建一個 QLabel 用於顯示圖片
        self.secondpage_picture_label_4 = QtWidgets.QLabel(self.page_4)
        self.secondpage_picture_label_4.setGeometry(0, 0, 1108, 670)  # 直接設置尺寸
        self.secondpage_picture_label_4.setScaledContents(True)  # 讓圖片自動縮放
        #self.secondpage_picture_label_4.setPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\底圖_4.png").scaled(1108, 670, QtCore.Qt.IgnoreAspectRatio))
        self.secondpage_picture_label_4.setAlignment(QtCore.Qt.AlignCenter)

        self.label = QtWidgets.QLabel(self.page_4)
        self.label.setGeometry(QtCore.QRect(500, 60, 171, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.calendarWidget = QtWidgets.QCalendarWidget(self.page_4)
        self.calendarWidget.setGeometry(QtCore.QRect(40, 240, 321, 241))
        self.calendarWidget.setObjectName("calendarWidget")

        self.use_time_graph = QtWidgets.QGraphicsView(self.page_4)
        self.use_time_graph.setGeometry(QtCore.QRect(410, 150, 281, 221))
        self.use_time_graph.setObjectName("use_time_graph")

        self.distance_graph = QtWidgets.QGraphicsView(self.page_4)
        self.distance_graph.setGeometry(QtCore.QRect(740, 150, 281, 221))
        self.distance_graph.setObjectName("distance_graph")

        self.blink_graph = QtWidgets.QGraphicsView(self.page_4)
        self.blink_graph.setGeometry(QtCore.QRect(410, 400, 281, 221))
        self.blink_graph.setObjectName("blink_graph")

        self.brightness_graph = QtWidgets.QGraphicsView(self.page_4)
        self.brightness_graph.setGeometry(QtCore.QRect(740, 400, 281, 221))
        self.brightness_graph.setObjectName("brightness_graph")

        self.send_to_line = QtWidgets.QToolButton(self.page_4)
        self.send_to_line.setGeometry(QtCore.QRect(810, 70, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.send_to_line.setFont(font)
        self.send_to_line.setObjectName("send_to_line")

        '''self.back_to_home = QtWidgets.QPushButton(self.page_4)
        self.back_to_home.setGeometry(QtCore.QRect(910, 60, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.back_to_home.setFont(font)
        self.back_to_home.setObjectName("back_to_home")'''


        self.choose_user = QtWidgets.QLabel(self.page_4)
        self.choose_user.setGeometry(QtCore.QRect(50, 190, 131, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.choose_user.setFont(font)
        self.choose_user.setObjectName("choose_user")

        self.nameBox_3 = QtWidgets.QComboBox(self.page_4)
        self.nameBox_3.setGeometry(QtCore.QRect(190, 190, 161, 22))
        self.nameBox_3.setObjectName("nameBox_3")

        #analysis：analysis_homebutton，之後可以把back的功能換掉
        self.analysis_homebutton = QtWidgets.QPushButton(self.page_4)
        self.analysis_homebutton.setGeometry(QtCore.QRect(1060, 10, 31, 31))
        self.analysis_homebutton.setText("")
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\home-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.analysis_homebutton.setIcon(icon)
        #self.analysis_homebutton.setIconSize(QtCore.QSize(30,30))
        self.analysis_homebutton.setObjectName("analysis_homebutton")
               # 設置樣式，讓按鈕背景透明並移除邊框
        self.analysis_homebutton.setStyleSheet("""
            QPushButton {
                background-color: transparent;  /* 背景透明 */
                border: none;                  /* 無邊框 */
            }
        """)

        self.stackedWidget.addWidget(self.page_4)

        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        
        # 創建一個 QLabel 用於顯示圖片
        self.secondpage_picture_label_5 = QtWidgets.QLabel(self.page_5)
        self.secondpage_picture_label_5.setGeometry(0, 0, 1108, 670)  # 直接設置尺寸
        self.secondpage_picture_label_5.setScaledContents(True)  # 讓圖片自動縮放
        #self.secondpage_picture_label_5.setPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\底圖_4.png").scaled(1108, 670, QtCore.Qt.IgnoreAspectRatio))
        self.secondpage_picture_label_5.setAlignment(QtCore.Qt.AlignCenter)
        
        #「姓名」標籤
        self.name_label3 = QtWidgets.QLabel(self.page_5)
        self.name_label3.setGeometry(QtCore.QRect(40, 45, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_label3.setFont(font)
        self.name_label3.setObjectName("name_label3") 

        #「姓名」輸入匡
        self.name_input = QtWidgets.QLineEdit(self.page_5)
        self.name_input.setGeometry(QtCore.QRect(130, 45, 113, 21))
        self.name_input.setObjectName("name_input")
        self.name_input.setPlaceholderText("範例：王大明")

        #「」
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.page_5)
        self.doubleSpinBox.setGeometry(QtCore.QRect(280, 790, 68, 24))
        self.doubleSpinBox.setObjectName("doubleSpinBox")

        #「使用者名稱」輸入匡
        self.user_name_input = QtWidgets.QLineEdit(self.page_5)
        self.user_name_input.setGeometry(QtCore.QRect(390, 45, 113, 21))
        self.user_name_input.setObjectName("user_name_input")
        self.user_name_input.setPlaceholderText("範例：Albert")

        #「使用者名稱」標籤
        self.user_name_label = QtWidgets.QLabel(self.page_5)
        self.user_name_label.setGeometry(QtCore.QRect(300, 45, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.user_name_label.setFont(font)
        self.user_name_label.setObjectName("user_name_label")

        #「生日」標籤
        self.birthday_label = QtWidgets.QLabel(self.page_5)
        self.birthday_label.setGeometry(QtCore.QRect(40, 90, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.birthday_label.setFont(font)
        self.birthday_label.setObjectName("birthday_label")

        #「生日」輸入匡
        self.birthday_input = QtWidgets.QLineEdit(self.page_5)
        self.birthday_input.setGeometry(QtCore.QRect(130, 90, 113, 21))
        self.birthday_input.setObjectName("birthday_input")
        self.birthday_input.setPlaceholderText("範例：20030722")

        #「性別」標籤
        self.sex_label = QtWidgets.QLabel(self.page_5)
        self.sex_label.setGeometry(QtCore.QRect(40, 135, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sex_label.setFont(font)
        self.sex_label.setObjectName("sex_label")

        #「性別」-男生按鈕
        self.sex_man_button = QtWidgets.QRadioButton(self.page_5)
        self.sex_man_button.setGeometry(QtCore.QRect(130, 135, 51, 20))
        self.sex_man_button.setObjectName("sex_man_button")

        #「性別」-女生按鈕
        self.sex_women_button = QtWidgets.QRadioButton(self.page_5)
        self.sex_women_button.setGeometry(QtCore.QRect(190, 135, 51, 20))
        self.sex_women_button.setObjectName("sex_women_button")

        #「性別」總按鈕
        self.sex_group = QtWidgets.QButtonGroup(self.page_5)
        self.sex_group.addButton(self.sex_women_button)
        self.sex_group.addButton(self.sex_man_button)

        #「line token」標籤
        self.line_token_label = QtWidgets.QLabel(self.page_5)
        self.line_token_label.setGeometry(QtCore.QRect(300, 90, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_token_label.setFont(font)
        self.line_token_label.setObjectName("line_token_label")

        #「line token」輸入匡
        self.line_token_input = QtWidgets.QLineEdit(self.page_5)
        self.line_token_input.setGeometry(QtCore.QRect(390, 90, 113, 21))
        self.line_token_input.setObjectName("line_token_input")
        self.line_token_input.setPlaceholderText("請複製貼上")

        #超連結說明的
        # 創建 QLabel 作為超連結
        self.link_edit = QtWidgets.QLabel(self.page_5)
        self.link_edit.setGeometry(QtCore.QRect(300, 115, 180, 20))
        # 設置 QLabel 為超連結格式
        self.link_edit.setText('<a href="https://drive.google.com/file/d/1x-pcbKEawdGpEtdDJnkO7-28H_URY7lm/view?usp=share_link">使用說明 (點擊我開啟PDF)</a>')
        self.link_edit.setOpenExternalLinks(True)  # 允許點擊後在外部瀏覽器中打開連結

        #「虛線7」
        self.line_7 = QtWidgets.QFrame(self.page_5)
        self.line_7.setGeometry(QtCore.QRect(30, 170, 441, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")

        #「右眼」標籤
        self.right_eye_label = QtWidgets.QLabel(self.page_5)
        self.right_eye_label.setGeometry(QtCore.QRect(295, 235, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.right_eye_label.setFont(font)
        self.right_eye_label.setObjectName("right_eye_label")

        #「右眼」遠視按鈕
        self.right_eye_out_button = QtWidgets.QRadioButton(self.page_5)
        self.right_eye_out_button.setGeometry(QtCore.QRect(340, 225, 61, 20))
        self.right_eye_out_button.setObjectName("right_eye_out_button")

        #「右眼」近視按鈕
        self.right_eye_in_button = QtWidgets.QRadioButton(self.page_5)
        self.right_eye_in_button.setGeometry(QtCore.QRect(340, 205, 61, 20))
        self.right_eye_in_button.setObjectName("right_eye_in_button")

        # 「右眼」近遠視總按鈕
        self.right_eye_group = QtWidgets.QButtonGroup(self.page_5)
        self.right_eye_group.addButton(self.right_eye_out_button)
        self.right_eye_group.addButton(self.right_eye_in_button)

        #「右眼度數」輸入匡
        self.right_eye_degree_input = QtWidgets.QLineEdit(self.page_5)
        self.right_eye_degree_input.setGeometry(QtCore.QRect(400, 215, 91, 20))
        self.right_eye_degree_input.setObjectName("right_eye_degree_input")
        self.right_eye_degree_input.setPlaceholderText("範例：200")

        #「右眼」閃光按鈕
        #還是有放按鈕鍵！如果按到無法取消，直接輸入0即可（預設也是0）
        self.right_eye_shine_button = QtWidgets.QRadioButton(self.page_5)
        self.right_eye_shine_button.setGeometry(QtCore.QRect(340, 265, 61, 20))
        self.right_eye_shine_button.setObjectName("right_eye_shine_button")

        # 「右眼」閃光總按鈕
        self.right_eye_shine_group = QtWidgets.QButtonGroup(self.page_5)
        self.right_eye_shine_group.addButton(self.right_eye_shine_button)
        

        #「右眼閃光」輸入匡
        self.right_eye_shine_input = QtWidgets.QLineEdit(self.page_5)
        self.right_eye_shine_input.setGeometry(QtCore.QRect(400, 265, 91, 20))
        self.right_eye_shine_input.setObjectName("right_eye_shine_input")
        self.right_eye_shine_input.setPlaceholderText("若無請填0")

        #「左眼」標籤
        self.left_eye_label = QtWidgets.QLabel(self.page_5)
        self.left_eye_label.setGeometry(QtCore.QRect(45, 235, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.left_eye_label.setFont(font)
        self.left_eye_label.setObjectName("left_eye_label")

        #「左眼」遠視按鈕
        self.left_eye_out_button = QtWidgets.QRadioButton(self.page_5)
        self.left_eye_out_button.setGeometry(QtCore.QRect(90, 225, 61, 20))
        self.left_eye_out_button.setObjectName("left_eye_out_button")

        #「左眼閃光」輸入匡
        self.left_eye_shine_input = QtWidgets.QLineEdit(self.page_5)
        self.left_eye_shine_input.setGeometry(QtCore.QRect(150, 265, 91, 20))
        self.left_eye_shine_input.setObjectName("left_eye_shine_input")
        self.left_eye_shine_input.setPlaceholderText("若無請填0")

        #「左眼度數」輸入匡
        self.left_eye_degree_input = QtWidgets.QLineEdit(self.page_5)
        self.left_eye_degree_input.setGeometry(QtCore.QRect(150, 215, 91, 20))
        self.left_eye_degree_input.setObjectName("left_eye_degree_input")
        self.left_eye_degree_input.setPlaceholderText("範例：200")

        #「左眼」近視按鈕
        self.left_eye_in_button = QtWidgets.QRadioButton(self.page_5)
        self.left_eye_in_button.setGeometry(QtCore.QRect(90, 205, 61, 20))
        self.left_eye_in_button.setObjectName("left_eye_in_button")

        #「左眼」近遠視總按鈕
        self.left_eye_group = QtWidgets.QButtonGroup(self.page_5)
        self.left_eye_group.addButton(self.left_eye_out_button)
        self.left_eye_group.addButton(self.left_eye_in_button)

        #「左眼」閃光按鈕
        self.left_eye_shine_button = QtWidgets.QRadioButton(self.page_5)
        self.left_eye_shine_button.setGeometry(QtCore.QRect(90, 265, 61, 20))
        self.left_eye_shine_button.setObjectName("left_eye_shine_button")
        

        # 「左眼」閃光總按鈕
        self.left_eye_shine_group = QtWidgets.QButtonGroup(self.page_5)
        self.left_eye_shine_group.addButton(self.left_eye_shine_button)

        '''此處五個為「眼睛用眼狀況」(左下角那一坨)'''

        # 配戴眼鏡的頻率（用眼狀況問題1）標籤
        self.eye_situation_label1 = QtWidgets.QLabel(self.page_5)
        self.eye_situation_label1.setGeometry(QtCore.QRect(40, 340, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_label1.setFont(font)
        self.eye_situation_label1.setObjectName("eye_situation_label1")   
        # 配戴隱眼的頻率（用眼狀況問題2）標籤
        self.eye_situation_label2 = QtWidgets.QLabel(self.page_5)
        self.eye_situation_label2.setGeometry(QtCore.QRect(40, 380, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_label2.setFont(font)
        self.eye_situation_label2.setObjectName("eye_situation_label2")
        # 眼睛乾澀頻率（用眼狀況問題3）標籤
        self.eye_situation_label3 = QtWidgets.QLabel(self.page_5)
        self.eye_situation_label3.setGeometry(QtCore.QRect(40, 420, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_label3.setFont(font)
        self.eye_situation_label3.setObjectName("eye_situation_label3")
        # 頭痛暈眩頻率（用眼狀況問題4）標籤
        self.eye_situation_label4 = QtWidgets.QLabel(self.page_5)
        self.eye_situation_label4.setGeometry(QtCore.QRect(40, 460, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_label4.setFont(font)
        self.eye_situation_label4.setObjectName("eye_situation_label4")
        # 眼睛疲勞頻率（用眼狀況問題5）標籤
        self.eye_situation_label5 = QtWidgets.QLabel(self.page_5)
        self.eye_situation_label5.setGeometry(QtCore.QRect(40, 500, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_label5.setFont(font)
        self.eye_situation_label5.setObjectName("eye_situation_label5")
        
        #點擊程度的上排數字標籤（1到10那個）
        self.eye_situation_upnumber_label = QtWidgets.QLabel(self.page_5)
        self.eye_situation_upnumber_label.setGeometry(QtCore.QRect(303, 327, 200, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_upnumber_label.setFont(font)
        self.eye_situation_upnumber_label.setObjectName("eye_situation_upnumber_label")
             
        # 創建 QButtonGroup 並將按鈕加入組
        self.eye_situation_button_group1 = QtWidgets.QButtonGroup(self.page_5)# 配戴眼鏡的頻率
        self.eye_situation_button_group2 = QtWidgets.QButtonGroup(self.page_5)# 配戴隱眼的頻率
        self.eye_situation_button_group3 = QtWidgets.QButtonGroup(self.page_5)# 眼睛乾澀頻率
        self.eye_situation_button_group4 = QtWidgets.QButtonGroup(self.page_5)# 頭痛暈眩頻率
        self.eye_situation_button_group5 = QtWidgets.QButtonGroup(self.page_5)# 眼睛疲勞頻率
        # 根據提供的 x 座標生成 QRadioButton
        self.temp_button1 = []  
        self.temp_button2 = []  
        self.temp_button3 = []  
        self.temp_button4 = []  
        self.temp_button5 = []  
        x_positions = [300, 319, 338, 357, 377, 397, 416, 437, 458, 480]  
        y_position1 = 340  
        y_position2 = 380  
        y_position3 = 420 
        y_position4 = 460
        y_position5 = 500
        for i, x in enumerate(x_positions, 1):  # 根據 x_positions 的位置來生成按鈕
            eye_situation_button1 = QtWidgets.QRadioButton(self.page_5)
            eye_situation_button1.setGeometry(QtCore.QRect(x, y_position1, 161, 22))
            eye_situation_button1.setObjectName(f"self.eye_situation_button1_{i}")
            self.temp_button1.append(eye_situation_button1)
            self.eye_situation_button_group1.addButton(eye_situation_button1,i)  # 將按鈕加入到 ButtonGroup
        for button in self.temp_button1:
            print(button.objectName())
        for i, x in enumerate(x_positions, 1):  
            eye_situation_button2 = QtWidgets.QRadioButton(self.page_5)
            eye_situation_button2.setGeometry(QtCore.QRect(x, y_position2, 161, 22))
            eye_situation_button2.setObjectName(f"eye_situation_button2_{i}")
            self.temp_button2.append(eye_situation_button2)
            self.eye_situation_button_group2.addButton(eye_situation_button2,i)  
        for i, x in enumerate(x_positions, 1):  
            eye_situation_button3 = QtWidgets.QRadioButton(self.page_5)
            eye_situation_button3.setGeometry(QtCore.QRect(x, y_position3, 161, 22))
            eye_situation_button3.setObjectName(f"eye_situation_button3_{i}")
            self.temp_button3.append(eye_situation_button3)
            self.eye_situation_button_group3.addButton(eye_situation_button3,i)  
        for i, x in enumerate(x_positions, 1):  
            eye_situation_button4 = QtWidgets.QRadioButton(self.page_5)
            eye_situation_button4.setGeometry(QtCore.QRect(x, y_position4, 161, 22))
            eye_situation_button4.setObjectName(f"eye_situation_button4_{i}")
            self.temp_button4.append(eye_situation_button4)
            self.eye_situation_button_group4.addButton(eye_situation_button4,i) 
        for i, x in enumerate(x_positions, 1):  
            eye_situation_button5 = QtWidgets.QRadioButton(self.page_5)
            eye_situation_button5.setGeometry(QtCore.QRect(x, y_position5, 161, 22))
            eye_situation_button5.setObjectName(f"eye_situation_button5_{i}")
            self.temp_button5.append(eye_situation_button5)
            self.eye_situation_button_group5.addButton(eye_situation_button5,i) 


        #
        self.line_8 = QtWidgets.QFrame(self.page_5)
        self.line_8.setGeometry(QtCore.QRect(30, 305, 441, 20))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")

        #
        self.line_9 = QtWidgets.QFrame(self.page_5)
        self.line_9.setGeometry(QtCore.QRect(30, 540, 441, 20))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        
        #「是否長時間使用電子產品」標籤
        self.use_situation_label1 = QtWidgets.QLabel(self.page_5)
        self.use_situation_label1.setGeometry(QtCore.QRect(560, 40, 330, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.use_situation_label1.setFont(font)
        self.use_situation_label1.setObjectName("use_situation_label1")

        #「是否長時間使用電子產品」-yes按鈕
        self.use_situation_yes_button1 = QtWidgets.QRadioButton(self.page_5)
        self.use_situation_yes_button1.setGeometry(QtCore.QRect(890, 40, 51, 20))
        self.use_situation_yes_button1.setObjectName("use_situation_yes_button1")

        #「是否長時間使用電子產品」不，按鈕
        self.use_situation_no_button1 = QtWidgets.QRadioButton(self.page_5)
        self.use_situation_no_button1.setGeometry(QtCore.QRect(950, 40, 51, 20))
        self.use_situation_no_button1.setObjectName("use_situation_no_button1")

        #「是否長時間使用電子產品」總按鈕
        self.use_situation1_group = QtWidgets.QButtonGroup(self.page_5)
        self.use_situation1_group.addButton(self.use_situation_yes_button1)
        self.use_situation1_group.addButton(self.use_situation_no_button1)

        

        #「使用設備時間」標籤
        self.use_situation_label2 = QtWidgets.QLabel(self.page_5)
        self.use_situation_label2.setGeometry(QtCore.QRect(560, 120, 340, 20)) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.use_situation_label2.setFont(font)
        self.use_situation_label2.setObjectName("use_situation_label2")

        #「使用設備時間」下拉式選單
        self.use_situation2_combobox = QtWidgets.QComboBox(self.page_5)
        self.use_situation2_combobox.setGeometry(QtCore.QRect(885, 120, 176, 26))
        self.use_situation2_combobox.setObjectName("use_situation2_combobox")
        self.use_situation2_combobox.addItem("")
        self.use_situation2_combobox.addItem("")
        self.use_situation2_combobox.addItem("")
        self.use_situation2_combobox.addItem("")
        self.use_situation2_combobox.addItem("")

        #「防藍光設備」標籤
        self.use_situation_label3 = QtWidgets.QLabel(self.page_5)
        self.use_situation_label3.setGeometry(QtCore.QRect(560, 80, 330, 20)) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.use_situation_label3.setFont(font)
        self.use_situation_label3.setObjectName("use_situation_label3")

        #「防藍光設備」是，按鈕
        self.use_situation_yes_button3 = QtWidgets.QRadioButton(self.page_5)
        self.use_situation_yes_button3.setGeometry(QtCore.QRect(890, 80, 51, 20))
        self.use_situation_yes_button3.setObjectName("use_situation_yes_button3")

        #「防藍光設備」不，按鈕
        self.use_situation_no_button3 = QtWidgets.QRadioButton(self.page_5)
        self.use_situation_no_button3.setGeometry(QtCore.QRect(950, 80, 51, 20))
        self.use_situation_no_button3.setObjectName("use_situation_no_button3")

        #「電子產品使用情況3」總按鈕
        self.use_situation3_group = QtWidgets.QButtonGroup(self.page_5)
        self.use_situation3_group.addButton(self.use_situation_yes_button3)
        self.use_situation3_group.addButton(self.use_situation_no_button3)

        
        #「調整顯示器頻率」（電子產品狀況4）標籤
        self.use_situation_label4 = QtWidgets.QLabel(self.page_5)
        self.use_situation_label4.setGeometry(QtCore.QRect(560, 200, 260, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.use_situation_label4.setFont(font)
        self.use_situation_label4.setObjectName("use_situation_label4")
        
        self.use_situation4_combobox = QtWidgets.QComboBox(self.page_5)
        self.use_situation4_combobox.setGeometry(QtCore.QRect(885, 200, 176, 26))
        self.use_situation4_combobox.setObjectName("use_situation4_combobox")
        self.use_situation4_combobox.addItem("")
        self.use_situation4_combobox.addItem("")
        self.use_situation4_combobox.addItem("")
        
        #「光線情形」（電子產品狀況5）標籤
        self.use_situation_label5 = QtWidgets.QLabel(self.page_5)
        self.use_situation_label5.setGeometry(QtCore.QRect(560, 160, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.use_situation_label5.setFont(font)
        self.use_situation_label5.setObjectName("use_situation_label5")
       
        self.use_situation5_combobox = QtWidgets.QComboBox(self.page_5)
        self.use_situation5_combobox.setGeometry(QtCore.QRect(885, 160, 176, 26))
        self.use_situation5_combobox.setObjectName("use_situation5_combobox")
        self.use_situation5_combobox.addItem("")
        self.use_situation5_combobox.addItem("")
        self.use_situation5_combobox.addItem("")
        self.use_situation5_combobox.addItem("")
        self.use_situation5_combobox.addItem("")
        self.use_situation5_combobox.addItem("")
        
        #「右中」虛線
        self.line_10 = QtWidgets.QFrame(self.page_5)
        self.line_10.setGeometry(QtCore.QRect(550, 230, 441, 20))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")

        #「保健食品」標籤
        self.habit_label1 = QtWidgets.QLabel(self.page_5)
        self.habit_label1.setGeometry(QtCore.QRect(560, 260, 250, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label1.setFont(font)
        self.habit_label1.setObjectName("habit_label1")

        #「保健食品」不，按鈕
        self.habit_no_button1 = QtWidgets.QRadioButton(self.page_5)
        self.habit_no_button1.setGeometry(QtCore.QRect(865, 260, 51, 20))
        self.habit_no_button1.setObjectName("habit_no_button1")

        #「保健食品」是，按鈕
        self.habit_yes_button1 = QtWidgets.QRadioButton(self.page_5)
        self.habit_yes_button1.setGeometry(QtCore.QRect(805, 260, 51, 20))
        self.habit_yes_button1.setObjectName("habit_yes_button1")

        #「保健食品」總按鈕
        self.habit1_group = QtWidgets.QButtonGroup(self.page_5)
        self.habit1_group.addButton(self.habit_yes_button1)
        self.habit1_group.addButton(self.habit_no_button1)

        #「檢查眼睛頻率」標籤
        self.habit_label2 = QtWidgets.QLabel(self.page_5)
        self.habit_label2.setGeometry(QtCore.QRect(560, 300, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label2.setFont(font)
        self.habit_label2.setObjectName("habit_label2")

        #「檢查眼睛頻率」下拉式選單
        self.habit_combobox2 = QtWidgets.QComboBox(self.page_5)
        self.habit_combobox2.setGeometry(QtCore.QRect(730, 300, 104, 26))
        self.habit_combobox2.setObjectName("habit_combobox2")
        self.habit_combobox2.addItem("")
        self.habit_combobox2.addItem("")
        self.habit_combobox2.addItem("")
        self.habit_combobox2.addItem("")

        #「右上」虛線
        self.line_6 = QtWidgets.QFrame(self.page_5)
        self.line_6.setGeometry(QtCore.QRect(550, 10, 441, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")

        #「左上」虛線
        self.line_1 = QtWidgets.QFrame(self.page_5)
        self.line_1.setGeometry(QtCore.QRect(30, 10, 441, 20))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")

        #「睡眠時長」標籤
        self.habit_label3 = QtWidgets.QLabel(self.page_5)
        self.habit_label3.setGeometry(QtCore.QRect(560, 340, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label3.setFont(font)
        self.habit_label3.setObjectName("habit_label3")

        #「睡眠時長」下拉式選單
        self.habit_combobox3 = QtWidgets.QComboBox(self.page_5)
        self.habit_combobox3.setGeometry(QtCore.QRect(730, 340, 104, 26))
        self.habit_combobox3.setObjectName("habit_combobox3")
        self.habit_combobox3.addItem("")
        self.habit_combobox3.addItem("")
        self.habit_combobox3.addItem("")
        self.habit_combobox3.addItem("")

        #「每週運動次數」標籤
        self.habit_label4 = QtWidgets.QLabel(self.page_5)
        self.habit_label4.setGeometry(QtCore.QRect(560, 380, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label4.setFont(font)
        self.habit_label4.setObjectName("habit_label4")

        #「每週運動次數」下拉式選單
        self.habit_combobox4 = QtWidgets.QComboBox(self.page_5)
        self.habit_combobox4.setGeometry(QtCore.QRect(730, 380, 104, 26))
        self.habit_combobox4.setObjectName("habit_combobox4")
        self.habit_combobox4.addItem("")
        self.habit_combobox4.addItem("")
        self.habit_combobox4.addItem("")
        self.habit_combobox4.addItem("")

        #「多久會休息」標籤
        self.habit_label5 = QtWidgets.QLabel(self.page_5)
        self.habit_label5.setGeometry(QtCore.QRect(560, 420, 291, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label5.setFont(font)
        self.habit_label5.setObjectName("habit_label5")

        #「多久會休息」下拉式選單
        self.habit_combobox5 = QtWidgets.QComboBox(self.page_5)
        self.habit_combobox5.setGeometry(QtCore.QRect(860, 420, 104, 26))
        self.habit_combobox5.setObjectName("habit_combobox5")
        self.habit_combobox5.addItem("")
        self.habit_combobox5.addItem("")
        self.habit_combobox5.addItem("")
        self.habit_combobox5.addItem("")
        self.habit_combobox5.addItem("")
        self.habit_combobox5.addItem("")
        self.habit_combobox5.addItem("")

        #「平均休息持續時間」標籤
        self.habit_label6 = QtWidgets.QLabel(self.page_5)
        self.habit_label6.setGeometry(QtCore.QRect(560, 460, 281, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label6.setFont(font)
        self.habit_label6.setObjectName("habit_label6")

        #「休息持續時間」下拉式選單
        self.habit_combobox6 = QtWidgets.QComboBox(self.page_5)
        self.habit_combobox6.setGeometry(QtCore.QRect(860, 460, 104, 26))
        self.habit_combobox6.setObjectName("habit_combobox6")
        self.habit_combobox6.addItem("")
        self.habit_combobox6.addItem("")
        self.habit_combobox6.addItem("")
        self.habit_combobox6.addItem("")

        #「休息習慣7」標籤
        self.habit_label7 = QtWidgets.QLabel(self.page_5)
        self.habit_label7.setGeometry(QtCore.QRect(560, 500, 271, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label7.setFont(font)
        self.habit_label7.setObjectName("habit_label7")

        #「生活習慣7-閉目養神」複選
        self.habit_close_checkbox7 = QtWidgets.QCheckBox(self.page_5)
        self.habit_close_checkbox7.setGeometry(QtCore.QRect(810, 500, 87, 20))
        self.habit_close_checkbox7.setObjectName("habit_close_checkbox7")

        #「生活習慣7-眼部運動」複選
        self.habit_exercise_checkbox7 = QtWidgets.QCheckBox(self.page_5)
        self.habit_exercise_checkbox7.setGeometry(QtCore.QRect(900, 500, 87, 20))
        self.habit_exercise_checkbox7.setObjectName("habit_exercise_checkbox7")

        #「生活習慣7-其他」複選
        self.habit_other_checkbox7 = QtWidgets.QCheckBox(self.page_5)
        self.habit_other_checkbox7.setGeometry(QtCore.QRect(990, 500, 87, 20))
        self.habit_other_checkbox7.setObjectName("habit_other_checkbox7")

        #「右下」虛線
        self.line_11 = QtWidgets.QFrame(self.page_5)
        self.line_11.setGeometry(QtCore.QRect(550, 540, 441, 20))
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")

        #註冊頁面「確定儲存」按鈕
        self.Savefile = QtWidgets.QPushButton(self.page_5)
        self.Savefile.setGeometry(QtCore.QRect(470, 570, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Savefile.setFont(font)
        self.Savefile.setObjectName("Savefile")

        #Sign up：signup_homebutton（要跳出一個警示匡說紀錄不保留喔）（save雖然會回去，但你填寫到一半沒有辦法回去）
        self.signup_homebutton = QtWidgets.QPushButton(self.page_5)
        self.signup_homebutton.setGeometry(QtCore.QRect(1060, 10, 31, 31))
        self.signup_homebutton.setText("")
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\home-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.signup_homebutton.setIcon(icon)
        #self.signup_homebutton.setIconSize(QtCore.QSize(30,30))
        self.signup_homebutton.setObjectName("signup_homebutton")
               # 設置樣式，讓按鈕背景透明並移除邊框
        self.signup_homebutton.setStyleSheet("""
            QPushButton {
                background-color: transparent;  /* 背景透明 */
                border: none;                  /* 無邊框 */
            }
        """)

        self.stackedWidget.addWidget(self.page_5)
        
        '''編輯頁面'''
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        #以下是page_6，編輯的介面
        #以下是page_6，編輯的介面
        #以下是page_6，編輯的介面
        
        # 創建一個 QLabel 用於顯示圖片
        self.secondpage_picture_label_6 = QtWidgets.QLabel(self.page_6)
        self.secondpage_picture_label_6.setGeometry(0, 0, 1108, 670)  # 直接設置尺寸
        self.secondpage_picture_label_6.setScaledContents(True)  # 讓圖片自動縮放
        #self.secondpage_picture_label_6.setPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\底圖_4.png").scaled(1108, 670, QtCore.Qt.IgnoreAspectRatio))
        self.secondpage_picture_label_6.setAlignment(QtCore.Qt.AlignCenter)
        
        #「姓名」標籤
        self.name_label3_edit = QtWidgets.QLabel(self.page_6)
        self.name_label3_edit.setGeometry(QtCore.QRect(40, 45, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_label3_edit.setFont(font)
        self.name_label3_edit.setObjectName("name_label3_edit") 
        #「姓名」輸入匡
        self.name_input_edit = QtWidgets.QLineEdit(self.page_6)
        self.name_input_edit.setGeometry(QtCore.QRect(130, 45, 113, 21))
        self.name_input_edit.setObjectName("name_input")
        self.name_input_edit.setPlaceholderText("範例：王大明")
   
        #「使用者名稱」標籤
        self.user_name_label_edit = QtWidgets.QLabel(self.page_6)
        self.user_name_label_edit.setGeometry(QtCore.QRect(300, 45, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.user_name_label_edit.setFont(font)
        self.user_name_label_edit.setObjectName("user_name_label_edit")
        #「選擇使用者名稱」下拉式選單  
        # 這裡跟前面的不一樣喔！
        self.nameBox_4 = QtWidgets.QComboBox(self.page_6)
        self.nameBox_4.setGeometry(QtCore.QRect(390, 45, 113, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.nameBox_4.setFont(font)
        self.nameBox_4.setObjectName("nameBox_4")
        self.nameBox_4.setPlaceholderText("選擇欲更新使用者")

        #「生日」標籤
        self.birthday_label_edit = QtWidgets.QLabel(self.page_6)
        self.birthday_label_edit.setGeometry(QtCore.QRect(40, 90, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.birthday_label_edit.setFont(font)
        self.birthday_label_edit.setObjectName("birthday_label_edit")
        #「生日」輸入匡
        self.birthday_input_edit = QtWidgets.QLineEdit(self.page_6)
        self.birthday_input_edit.setGeometry(QtCore.QRect(130, 90, 113, 21))
        self.birthday_input_edit.setObjectName("birthday_input_edit")
        self.birthday_input_edit.setPlaceholderText("範例：20030722")

        #「性別」標籤
        self.sex_label_edit = QtWidgets.QLabel(self.page_6)
        self.sex_label_edit.setGeometry(QtCore.QRect(40, 135, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sex_label_edit.setFont(font)
        self.sex_label_edit.setObjectName("sex_label_edit")
        #「性別」-男生按鈕
        self.sex_man_button_edit = QtWidgets.QRadioButton(self.page_6)
        self.sex_man_button_edit.setGeometry(QtCore.QRect(130, 135, 51, 20))
        self.sex_man_button_edit.setObjectName("sex_man_button_edit")
        #「性別」-女生按鈕
        self.sex_women_button_edit = QtWidgets.QRadioButton(self.page_6)
        self.sex_women_button_edit.setGeometry(QtCore.QRect(190, 135, 51, 20))
        self.sex_women_button_edit.setObjectName("sex_women_button_edit")
        #「性別」總按鈕
        self.sex_group_edit = QtWidgets.QButtonGroup(self.page_6)
        self.sex_group_edit.addButton(self.sex_women_button_edit)
        self.sex_group_edit.addButton(self.sex_man_button_edit)
        
        #「line token」標籤
        self.line_token_label_edit = QtWidgets.QLabel(self.page_6)
        self.line_token_label_edit.setGeometry(QtCore.QRect(300, 90, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_token_label_edit.setFont(font)
        self.line_token_label_edit.setObjectName("line_token_label_edit")
        #「line token」輸入匡
        self.line_token_input_edit = QtWidgets.QLineEdit(self.page_6)
        self.line_token_input_edit.setGeometry(QtCore.QRect(390, 90, 113, 21))
        self.line_token_input_edit.setObjectName("line_token_input_edit")
        self.line_token_input_edit.setPlaceholderText("請複製貼上")
        
        #超連結說明的
        # 創建 QLabel 作為超連結
        self.link_edit = QtWidgets.QLabel(self.page_5)
        self.link_edit.setGeometry(QtCore.QRect(300, 115, 180, 20))
        # 設置 QLabel 為超連結格式
        self.link_edit.setText('<a href="https://drive.google.com/file/d/1x-pcbKEawdGpEtdDJnkO7-28H_URY7lm/view?usp=share_link">使用說明 (點擊我開啟PDF)</a>')
        self.link_edit.setOpenExternalLinks(True)  # 允許點擊後在外部瀏覽器中打開連結
   
        #「右眼」標籤
        self.right_eye_label_edit = QtWidgets.QLabel(self.page_6)
        self.right_eye_label_edit.setGeometry(QtCore.QRect(295, 235, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.right_eye_label_edit.setFont(font)
        self.right_eye_label_edit.setObjectName("right_eye_label_edit")
        #「右眼」遠視按鈕
        self.right_eye_out_button_edit = QtWidgets.QRadioButton(self.page_6)
        self.right_eye_out_button_edit.setGeometry(QtCore.QRect(340, 225, 61, 20))
        self.right_eye_out_button_edit.setObjectName("right_eye_out_button_edit")
        #「右眼」近視按鈕
        self.right_eye_in_button_edit = QtWidgets.QRadioButton(self.page_6)
        self.right_eye_in_button_edit.setGeometry(QtCore.QRect(340, 205, 61, 20))
        self.right_eye_in_button_edit.setObjectName("right_eye_in_button_edit")
        # 「右眼」近遠視總按鈕
        self.right_eye_group_edit = QtWidgets.QButtonGroup(self.page_6)
        self.right_eye_group_edit.addButton(self.right_eye_out_button)
        self.right_eye_group_edit.addButton(self.right_eye_in_button)

        #「右眼度數」輸入匡
        self.right_eye_degree_input_edit = QtWidgets.QLineEdit(self.page_6)
        self.right_eye_degree_input_edit.setGeometry(QtCore.QRect(400, 215, 91, 20))
        self.right_eye_degree_input_edit.setObjectName("right_eye_degree_input_edit")
        self.right_eye_degree_input_edit.setPlaceholderText("範例：200")

        #「右眼」閃光按鈕
        #還是有放按鈕鍵！如果按到無法取消，直接輸入0即可（預設也是0）
        self.right_eye_shine_button_edit = QtWidgets.QRadioButton(self.page_6)
        self.right_eye_shine_button_edit.setGeometry(QtCore.QRect(340, 265, 61, 20))
        self.right_eye_shine_button_edit.setObjectName("right_eye_shine_button_edit")
        # 「右眼」閃光總按鈕
        self.right_eye_shine_group_edit = QtWidgets.QButtonGroup(self.page_6)
        self.right_eye_shine_group_edit.addButton(self.right_eye_shine_button_edit)

        #「右眼閃光」輸入匡
        self.right_eye_shine_input_edit = QtWidgets.QLineEdit(self.page_6)
        self.right_eye_shine_input_edit.setGeometry(QtCore.QRect(400, 265, 91, 20))
        self.right_eye_shine_input_edit.setObjectName("right_eye_shine_input_edit")
        self.right_eye_shine_input_edit.setPlaceholderText("若無請填0")

        #「左眼」標籤
        self.left_eye_label_edit = QtWidgets.QLabel(self.page_6)
        self.left_eye_label_edit.setGeometry(QtCore.QRect(45, 235, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.left_eye_label_edit.setFont(font)
        self.left_eye_label_edit.setObjectName("left_eye_label_edit")
        #「左眼」遠視按鈕
        self.left_eye_out_button_edit = QtWidgets.QRadioButton(self.page_6)
        self.left_eye_out_button_edit.setGeometry(QtCore.QRect(90, 225, 61, 20))
        self.left_eye_out_button_edit.setObjectName("left_eye_out_button_edit")
        #「左眼」近視按鈕
        self.left_eye_in_button_edit = QtWidgets.QRadioButton(self.page_6)
        self.left_eye_in_button_edit.setGeometry(QtCore.QRect(90, 205, 61, 20))
        self.left_eye_in_button_edit.setObjectName("left_eye_in_button_edit")
        #「左眼」近遠視總按鈕
        self.left_eye_group_edit = QtWidgets.QButtonGroup(self.page_6)
        self.left_eye_group_edit.addButton(self.left_eye_out_button_edit)
        self.left_eye_group_edit.addButton(self.left_eye_in_button_edit)

        #「左眼度數」輸入匡
        self.left_eye_degree_input_edit = QtWidgets.QLineEdit(self.page_6)
        self.left_eye_degree_input_edit.setGeometry(QtCore.QRect(150, 215, 91, 20))
        self.left_eye_degree_input_edit.setObjectName("left_eye_degree_input_edit")
        self.left_eye_degree_input_edit.setPlaceholderText("範例：200")

        #「左眼」閃光按鈕
        self.left_eye_shine_button_edit = QtWidgets.QRadioButton(self.page_6)
        self.left_eye_shine_button_edit.setGeometry(QtCore.QRect(90, 265, 61, 20))
        self.left_eye_shine_button_edit.setObjectName("left_eye_shine_button_edit")
        # 「左眼」閃光總按鈕
        self.left_eye_shine_group_edit = QtWidgets.QButtonGroup(self.page_6)
        self.left_eye_shine_group_edit.addButton(self.left_eye_shine_button_edit)

        #「左眼閃光」輸入匡
        self.left_eye_shine_input_edit = QtWidgets.QLineEdit(self.page_6)
        self.left_eye_shine_input_edit.setGeometry(QtCore.QRect(150, 265, 91, 20))
        self.left_eye_shine_input_edit.setObjectName("left_eye_shine_input_edit")
        self.left_eye_shine_input_edit.setPlaceholderText("若無請填0")

        #此處五個為「眼睛用眼狀況」(左下角那一坨)
        # 配戴眼鏡的頻率（用眼狀況問題1）標籤
        self.eye_situation_label1_edit = QtWidgets.QLabel(self.page_6)
        self.eye_situation_label1_edit.setGeometry(QtCore.QRect(40, 340, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_label1_edit.setFont(font)
        self.eye_situation_label1_edit.setObjectName("eye_situation_label1_edit")   

        # 配戴隱眼的頻率（用眼狀況問題2）標籤
        self.eye_situation_label2_edit = QtWidgets.QLabel(self.page_6)
        self.eye_situation_label2_edit.setGeometry(QtCore.QRect(40, 380, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_label2_edit.setFont(font)
        self.eye_situation_label2_edit.setObjectName("eye_situation_label2_edit")

        # 眼睛乾澀頻率（用眼狀況問題3）標籤
        self.eye_situation_label3_edit = QtWidgets.QLabel(self.page_6)
        self.eye_situation_label3_edit.setGeometry(QtCore.QRect(40, 420, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_label3_edit.setFont(font)
        self.eye_situation_label3_edit.setObjectName("eye_situation_label_edit")

        # 頭痛暈眩頻率（用眼狀況問題4）標籤
        self.eye_situation_label4_edit = QtWidgets.QLabel(self.page_6)
        self.eye_situation_label4_edit.setGeometry(QtCore.QRect(40, 460, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_label4_edit.setFont(font)
        self.eye_situation_label4_edit.setObjectName("eye_situation_label4_edit")

        # 眼睛疲勞頻率（用眼狀況問題5）標籤
        self.eye_situation_label5_edit = QtWidgets.QLabel(self.page_6)
        self.eye_situation_label5_edit.setGeometry(QtCore.QRect(40, 500, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_label5_edit.setFont(font)
        self.eye_situation_label5_edit.setObjectName("eye_situation_label5_edit")

        #點擊程度的上排數字標籤（1到10那個）
        self.eye_situation_upnumber_label_edit = QtWidgets.QLabel(self.page_6)
        self.eye_situation_upnumber_label_edit.setGeometry(QtCore.QRect(303, 327, 200, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_upnumber_label_edit.setFont(font)
        self.eye_situation_upnumber_label_edit.setObjectName("eye_situation_upnumber_label_edit")
             
        # 創建 QButtonGroup 並將按鈕加入組
        self.eye_situation_button_group1_edit = QtWidgets.QButtonGroup(self.page_6)# 配戴眼鏡的頻率
        self.eye_situation_button_group2_edit = QtWidgets.QButtonGroup(self.page_6)# 配戴隱眼的頻率
        self.eye_situation_button_group3_edit = QtWidgets.QButtonGroup(self.page_6)# 眼睛乾澀頻率
        self.eye_situation_button_group4_edit = QtWidgets.QButtonGroup(self.page_6)# 頭痛暈眩頻率
        self.eye_situation_button_group5_edit = QtWidgets.QButtonGroup(self.page_6)# 眼睛疲勞頻率
        # 根據提供的 x 座標生成 QRadioButton
        self.temp_button1_edit = []  
        self.temp_button2_edit = []  
        self.temp_button3_edit = []  
        self.temp_button4_edit = []  
        self.temp_button5_edit = []  
        x_positions = [300, 319, 338, 357, 377, 397, 416, 437, 458, 480]  
        y_position1 = 340  
        y_position2 = 380  
        y_position3 = 420 
        y_position4 = 460
        y_position5 = 500
        for i, x in enumerate(x_positions, 1):  # 根據 x_positions 的位置來生成按鈕
            eye_situation_button1_edit = QtWidgets.QRadioButton(self.page_6)
            eye_situation_button1_edit.setGeometry(QtCore.QRect(x, y_position1, 161, 22))
            eye_situation_button1_edit.setObjectName(f"self.eye_situation_button1_{i}_edit")
            self.temp_button1_edit.append(eye_situation_button1_edit)
            self.eye_situation_button_group1_edit.addButton(eye_situation_button1_edit,i)  # 將按鈕加入到 ButtonGroup
        for i, x in enumerate(x_positions, 1):  
            eye_situation_button2_edit = QtWidgets.QRadioButton(self.page_6)
            eye_situation_button2_edit.setGeometry(QtCore.QRect(x, y_position2, 161, 22))
            eye_situation_button2_edit.setObjectName(f"eye_situation_button2_{i}_edit")
            self.temp_button2_edit.append(eye_situation_button2_edit)
            self.eye_situation_button_group2_edit.addButton(eye_situation_button2_edit,i)  
        for i, x in enumerate(x_positions, 1):  
            eye_situation_button3_edit = QtWidgets.QRadioButton(self.page_6)
            eye_situation_button3_edit.setGeometry(QtCore.QRect(x, y_position3, 161, 22))
            eye_situation_button3_edit.setObjectName(f"eye_situation_button3_{i}_edit")
            self.temp_button3_edit.append(eye_situation_button3_edit)
            self.eye_situation_button_group3_edit.addButton(eye_situation_button3_edit,i)  
        for i, x in enumerate(x_positions, 1):  
            eye_situation_button4_edit = QtWidgets.QRadioButton(self.page_6)
            eye_situation_button4_edit.setGeometry(QtCore.QRect(x, y_position4, 161, 22))
            eye_situation_button4_edit.setObjectName(f"eye_situation_button4_{i}_edit")
            self.temp_button4_edit.append(eye_situation_button4_edit)
            self.eye_situation_button_group4_edit.addButton(eye_situation_button4_edit,i) 
        for i, x in enumerate(x_positions, 1):  
            eye_situation_button5_edit = QtWidgets.QRadioButton(self.page_6)
            eye_situation_button5_edit.setGeometry(QtCore.QRect(x, y_position5, 161, 22))
            eye_situation_button5_edit.setObjectName(f"eye_situation_button5_{i}_edit")
            self.temp_button5_edit.append(eye_situation_button5_edit)
            self.eye_situation_button_group5_edit.addButton(eye_situation_button5_edit,i)

        
        # 電子產品狀況（右上角那一坨）
        # 電子產品狀況（右上角那一坨）
        # 電子產品狀況（右上角那一坨）
        #「是否長時間使用電子產品」標籤
        self.use_situation_label1_edit = QtWidgets.QLabel(self.page_6)
        self.use_situation_label1_edit.setGeometry(QtCore.QRect(560, 40, 330, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.use_situation_label1_edit.setFont(font)
        self.use_situation_label1_edit.setObjectName("use_situation_label1_edit")

        #「是否長時間使用電子產品」-yes按鈕
        self.use_situation_yes_button1_edit = QtWidgets.QRadioButton(self.page_6)
        self.use_situation_yes_button1_edit.setGeometry(QtCore.QRect(890, 40, 51, 20))
        self.use_situation_yes_button1_edit.setObjectName("use_situation_yes_button1_edit")

        #「是否長時間使用電子產品」不，按鈕
        self.use_situation_no_button1_edit = QtWidgets.QRadioButton(self.page_6)
        self.use_situation_no_button1_edit.setGeometry(QtCore.QRect(950, 40, 51, 20))
        self.use_situation_no_button1_edit.setObjectName("use_situation_no_button1_edit")

        #「是否長時間使用電子產品」總按鈕
        self.use_situation1_group_edit = QtWidgets.QButtonGroup(self.page_6)
        self.use_situation1_group_edit.addButton(self.use_situation_yes_button1_edit)
        self.use_situation1_group_edit.addButton(self.use_situation_no_button1_edit)

        #「使用設備時間」標籤
        self.use_situation_label2_edit = QtWidgets.QLabel(self.page_6)
        self.use_situation_label2_edit.setGeometry(QtCore.QRect(560, 120, 340, 20)) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.use_situation_label2_edit.setFont(font)
        self.use_situation_label2_edit.setObjectName("use_situation_label2_edit")

        #「使用設備時間」下拉式選單
        self.use_situation2_combobox_edit = QtWidgets.QComboBox(self.page_6)
        self.use_situation2_combobox_edit.setGeometry(QtCore.QRect(885, 120, 176, 26))
        self.use_situation2_combobox_edit.setObjectName("use_situation2_combobox_edit")
        self.use_situation2_combobox_edit.addItem("")
        self.use_situation2_combobox_edit.addItem("")
        self.use_situation2_combobox_edit.addItem("")
        self.use_situation2_combobox_edit.addItem("")
        self.use_situation2_combobox_edit.addItem("")

        #「防藍光設備」標籤
        self.use_situation_label3_edit = QtWidgets.QLabel(self.page_6)
        self.use_situation_label3_edit.setGeometry(QtCore.QRect(560, 80, 330, 20)) 
        font = QtGui.QFont()
        font.setPointSize(10)
        self.use_situation_label3_edit.setFont(font)
        self.use_situation_label3_edit.setObjectName("use_situation_label3_edit")

        #「防藍光設備」是，按鈕
        self.use_situation_yes_button3_edit = QtWidgets.QRadioButton(self.page_6)
        self.use_situation_yes_button3_edit.setGeometry(QtCore.QRect(890, 80, 51, 20))
        self.use_situation_yes_button3_edit.setObjectName("use_situation_yes_button3_edit")

        #「防藍光設備」不，按鈕
        self.use_situation_no_button3_edit = QtWidgets.QRadioButton(self.page_6)
        self.use_situation_no_button3_edit.setGeometry(QtCore.QRect(950, 80, 51, 20))
        self.use_situation_no_button3_edit.setObjectName("use_situation_no_button3_edit")

        #「電子產品使用情況3」總按鈕
        self.use_situation3_group_edit = QtWidgets.QButtonGroup(self.page_6)
        self.use_situation3_group_edit.addButton(self.use_situation_yes_button3_edit)
        self.use_situation3_group_edit.addButton(self.use_situation_no_button3_edit)

        #「調整顯示器頻率」（電子產品狀況4）標籤
        self.use_situation_label4_edit = QtWidgets.QLabel(self.page_6)
        self.use_situation_label4_edit.setGeometry(QtCore.QRect(560, 200, 260, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.use_situation_label4_edit.setFont(font)
        self.use_situation_label4_edit.setObjectName("use_situation_label4_edit")
        
        self.use_situation4_combobox_edit = QtWidgets.QComboBox(self.page_6)
        self.use_situation4_combobox_edit.setGeometry(QtCore.QRect(885, 200, 176, 26))
        self.use_situation4_combobox_edit.setObjectName("use_situation4_combobox_edit")
        self.use_situation4_combobox_edit.addItem("")
        self.use_situation4_combobox_edit.addItem("")
        self.use_situation4_combobox_edit.addItem("")
        
        #「光線情形」（電子產品狀況5）標籤
        self.use_situation_label5_edit = QtWidgets.QLabel(self.page_6)
        self.use_situation_label5_edit.setGeometry(QtCore.QRect(560, 160, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.use_situation_label5_edit.setFont(font)
        self.use_situation_label5_edit.setObjectName("use_situation_label5_edit")

        self.use_situation5_combobox_edit = QtWidgets.QComboBox(self.page_6)
        self.use_situation5_combobox_edit.setGeometry(QtCore.QRect(885, 160, 176, 26))
        self.use_situation5_combobox_edit.setObjectName("use_situation5_combobox_edit")
        self.use_situation5_combobox_edit.addItem("")
        self.use_situation5_combobox_edit.addItem("")
        self.use_situation5_combobox_edit.addItem("")
        self.use_situation5_combobox_edit.addItem("")
        self.use_situation5_combobox_edit.addItem("")
        self.use_situation5_combobox_edit.addItem("")
        
    
        # 生活習慣（右下角那一坨）
        #「保健食品」（生活習慣1）標籤
        self.habit_label1_edit = QtWidgets.QLabel(self.page_6)
        self.habit_label1_edit.setGeometry(QtCore.QRect(560, 260, 250, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label1_edit.setFont(font)
        self.habit_label1_edit.setObjectName("habit_label1_edit")
        #「保健食品」是，按鈕（生活習慣1）
        self.habit_yes_button1_edit = QtWidgets.QRadioButton(self.page_6)
        self.habit_yes_button1_edit.setGeometry(QtCore.QRect(805, 260, 51, 20))
        self.habit_yes_button1_edit.setObjectName("habit_yes_button1_edit")
        #「保健食品」不，按鈕（生活習慣1）
        self.habit_no_button1_edit = QtWidgets.QRadioButton(self.page_6)
        self.habit_no_button1_edit.setGeometry(QtCore.QRect(865, 260, 51, 20))
        self.habit_no_button1_edit.setObjectName("habit_no_button1_edit")
        #「保健食品」總按鈕（生活習慣1）
        self.habit1_group_edit = QtWidgets.QButtonGroup(self.page_6)
        self.habit1_group_edit.addButton(self.habit_yes_button1_edit)
        self.habit1_group_edit.addButton(self.habit_no_button1_edit)

        #「檢查眼睛頻率」（生活習慣2）標籤
        self.habit_label2_edit = QtWidgets.QLabel(self.page_6)
        self.habit_label2_edit.setGeometry(QtCore.QRect(560, 300, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label2_edit.setFont(font)
        self.habit_label2_edit.setObjectName("habit_label2_edit")
        #「檢查眼睛頻率」（生活習慣2）下拉式選單
        self.habit_combobox2_edit = QtWidgets.QComboBox(self.page_6)
        self.habit_combobox2_edit.setGeometry(QtCore.QRect(730, 300, 104, 26))
        self.habit_combobox2_edit.setObjectName("habit_combobox2_edit")
        self.habit_combobox2_edit.addItem("")
        self.habit_combobox2_edit.addItem("")
        self.habit_combobox2_edit.addItem("")
        self.habit_combobox2_edit.addItem("")

        #「睡眠時長」（生活習慣3）標籤
        self.habit_label3_edit = QtWidgets.QLabel(self.page_6)
        self.habit_label3_edit.setGeometry(QtCore.QRect(560, 340, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label3_edit.setFont(font)
        self.habit_label3_edit.setObjectName("habit_label3_edit")
        #「睡眠時長」（生活習慣3）下拉式選單
        self.habit_combobox3_edit = QtWidgets.QComboBox(self.page_6)
        self.habit_combobox3_edit.setGeometry(QtCore.QRect(730, 340, 104, 26))
        self.habit_combobox3_edit.setObjectName("habit_combobox3_edit")
        self.habit_combobox3_edit.addItem("")
        self.habit_combobox3_edit.addItem("")
        self.habit_combobox3_edit.addItem("")
        self.habit_combobox3_edit.addItem("")

        #「每週運動次數」（生活習慣4）標籤
        self.habit_label4_edit = QtWidgets.QLabel(self.page_6)
        self.habit_label4_edit.setGeometry(QtCore.QRect(560, 380, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label4_edit.setFont(font)
        self.habit_label4_edit.setObjectName("habit_label4_edit")
        #「每週運動次數」（生活習慣4）下拉式選單
        self.habit_combobox4_edit = QtWidgets.QComboBox(self.page_6)
        self.habit_combobox4_edit.setGeometry(QtCore.QRect(730, 380, 104, 26))
        self.habit_combobox4_edit.setObjectName("habit_combobox4_edit")
        self.habit_combobox4_edit.addItem("")
        self.habit_combobox4_edit.addItem("")
        self.habit_combobox4_edit.addItem("")
        self.habit_combobox4_edit.addItem("")

        #「多久會休息」（生活習慣5）標籤
        self.habit_label5_edit = QtWidgets.QLabel(self.page_6)
        self.habit_label5_edit.setGeometry(QtCore.QRect(560, 420, 291, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label5_edit.setFont(font)
        self.habit_label5_edit.setObjectName("habit_label5_edit")
        #「多久會休息」（生活習慣5）下拉式選單
        self.habit_combobox5_edit = QtWidgets.QComboBox(self.page_6)
        self.habit_combobox5_edit.setGeometry(QtCore.QRect(860, 420, 104, 26))
        self.habit_combobox5_edit.setObjectName("habit_combobox5_edit")
        self.habit_combobox5_edit.addItem("")
        self.habit_combobox5_edit.addItem("")
        self.habit_combobox5_edit.addItem("")
        self.habit_combobox5_edit.addItem("")
        self.habit_combobox5_edit.addItem("")
        self.habit_combobox5_edit.addItem("")
        self.habit_combobox5_edit.addItem("")

        #「平均休息持續時間」（生活習慣6）標籤
        self.habit_label6_edit = QtWidgets.QLabel(self.page_6)
        self.habit_label6_edit.setGeometry(QtCore.QRect(560, 460, 281, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label6_edit.setFont(font)
        self.habit_label6_edit.setObjectName("habit_label6_edit")
        #「休息持續時間」（生活習慣6）下拉式選單
        self.habit_combobox6_edit = QtWidgets.QComboBox(self.page_6)
        self.habit_combobox6_edit.setGeometry(QtCore.QRect(860, 460, 104, 26))
        self.habit_combobox6_edit.setObjectName("habit_combobox6_edit")
        self.habit_combobox6_edit.addItem("")
        self.habit_combobox6_edit.addItem("")
        self.habit_combobox6_edit.addItem("")
        self.habit_combobox6_edit.addItem("")

        #「休息方式為何」（生活習慣7）標籤
        self.habit_label7_edit = QtWidgets.QLabel(self.page_6)
        self.habit_label7_edit.setGeometry(QtCore.QRect(560, 500, 271, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.habit_label7_edit.setFont(font)
        self.habit_label7_edit.setObjectName("habit_label7_edit")
        #「休息方式為何-閉目養神」（生活習慣7）複選
        self.habit_close_checkbox7_edit = QtWidgets.QCheckBox(self.page_6)
        self.habit_close_checkbox7_edit.setGeometry(QtCore.QRect(810, 500, 87, 20))
        self.habit_close_checkbox7_edit.setObjectName("habit_close_checkbox7_edit")
        #「休息方式為何-眼部運動」（生活習慣7）複選
        self.habit_exercise_checkbox7_edit = QtWidgets.QCheckBox(self.page_6)
        self.habit_exercise_checkbox7_edit.setGeometry(QtCore.QRect(900, 500, 87, 20))
        self.habit_exercise_checkbox7_edit.setObjectName("habit_exercise_checkbox7_edit")
        #「休息方式為何-其他」（生活習慣7）複選
        self.habit_other_checkbox7_edit = QtWidgets.QCheckBox(self.page_6)
        self.habit_other_checkbox7_edit.setGeometry(QtCore.QRect(990, 500, 87, 20))
        self.habit_other_checkbox7_edit.setObjectName("habit_other_checkbox7_edit")

        #「左上」虛線
        self.line_1_edit = QtWidgets.QFrame(self.page_6)
        self.line_1_edit.setGeometry(QtCore.QRect(30, 10, 441, 20))
        self.line_1_edit.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1_edit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1_edit.setObjectName("line_1_edit")
        #「右上」虛線
        self.line_6_edit = QtWidgets.QFrame(self.page_6)
        self.line_6_edit.setGeometry(QtCore.QRect(550, 10, 441, 20))
        self.line_6_edit.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6_edit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6_edit.setObjectName("line_6_edit")
        #「虛線7」
        self.line_7_edit = QtWidgets.QFrame(self.page_6)
        self.line_7_edit.setGeometry(QtCore.QRect(30, 170, 441, 20))
        self.line_7_edit.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7_edit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7_edit.setObjectName("line_7_edit")
        # 虛線
        self.line_8_edit = QtWidgets.QFrame(self.page_6)
        self.line_8_edit.setGeometry(QtCore.QRect(30, 305, 441, 20))
        self.line_8_edit.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8_edit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8_edit.setObjectName("line_8_edit")
        # 虛線
        self.line_9_edit = QtWidgets.QFrame(self.page_6)
        self.line_9_edit.setGeometry(QtCore.QRect(30, 540, 441, 20))
        self.line_9_edit.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9_edit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9_edit.setObjectName("line_9_edit")
        #「右中」虛線
        self.line_10_edit = QtWidgets.QFrame(self.page_6)
        self.line_10_edit.setGeometry(QtCore.QRect(550, 230, 441, 20))
        self.line_10_edit.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10_edit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10_edit.setObjectName("line_10_edit")
        #「右下」虛線
        self.line_11_edit = QtWidgets.QFrame(self.page_6)
        self.line_11_edit.setGeometry(QtCore.QRect(550, 540, 441, 20))
        self.line_11_edit.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11_edit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11_edit.setObjectName("line_11_edit")
        
    

        # 編輯頁面的「儲存按鈕」
        self.Savefile_edit = QtWidgets.QPushButton(self.page_6)
        self.Savefile_edit.setGeometry(QtCore.QRect(330, 575, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Savefile_edit.setFont(font)
        self.Savefile_edit.setObjectName("Savefile_edit")
        # 編輯頁面的「刪除按鈕」
        self.deletefile_edit = QtWidgets.QPushButton(self.page_6)
        self.deletefile_edit.setGeometry(QtCore.QRect(560, 575, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.deletefile_edit.setFont(font)
        self.deletefile_edit.setObjectName("deletefile_edit")     
        # 編輯頁面的「edit1_homebutton」
        self.edit1_homebutton = QtWidgets.QPushButton(self.page_6)
        self.edit1_homebutton.setGeometry(QtCore.QRect(1060, 10, 31, 31))
        self.edit1_homebutton.setText("")
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\home-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.edit1_homebutton.setIcon(icon)
        #self.edit1_homebutton.setIconSize(QtCore.QSize(30,30))
        self.edit1_homebutton.setObjectName("edit1_homebutton")
               # 設置樣式，讓按鈕背景透明並移除邊框
        self.edit1_homebutton.setStyleSheet("""
            QPushButton {
                background-color: transparent;  /* 背景透明 */
                border: none;                  /* 無邊框 */
            }
        """)

        '''後側介面'''
        self.stackedWidget.addWidget(self.page_6)
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        
        # 創建一個 QLabel 用於顯示圖片
        self.secondpage_picture_label_7 = QtWidgets.QLabel(self.page_7)
        self.secondpage_picture_label_7.setGeometry(0, 0, 1108, 670)  # 直接設置尺寸
        self.secondpage_picture_label_7.setScaledContents(True)  # 讓圖片自動縮放
        #self.secondpage_picture_label_7.setPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\底圖_4.png").scaled(1108, 670, QtCore.Qt.IgnoreAspectRatio))
        self.secondpage_picture_label_7.setAlignment(QtCore.Qt.AlignCenter)
        
        #「頂端文字說明」（那一大串的那個）
        self.top_label = QtWidgets.QLabel(self.page_7)
        self.top_label.setEnabled(True)
        self.top_label.setGeometry(QtCore.QRect(160, 30, 850, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.top_label.setFont(font)
        self.top_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.top_label.setOpenExternalLinks(False)
        self.top_label.setObjectName("top_label")

        #「虛線」（中間那條垂直虛線）
        self.line = QtWidgets.QFrame(self.page_7)
        self.line.setGeometry(QtCore.QRect(540, 150, 20, 441))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        #順序為由左至右，由上到下！
        #「問題1」標籤
        self.question_1_label = QtWidgets.QLabel(self.page_7)
        self.question_1_label.setGeometry(QtCore.QRect(80, 160, 234, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_1_label.setFont(font)
        self.question_1_label.setObjectName("question_1_label")

        #「問題1」下拉式選單
        self.question_1_comboBox = QtWidgets.QComboBox(self.page_7)
        self.question_1_comboBox.setGeometry(QtCore.QRect(340, 160, 181, 26))
        self.question_1_comboBox.setObjectName("question_1_comboBox")
        self.question_1_comboBox.addItem("")
        self.question_1_comboBox.addItem("")
        self.question_1_comboBox.addItem("")
        self.question_1_comboBox.addItem("")

        #「問題2」標籤
        self.question_2_label = QtWidgets.QLabel(self.page_7)
        self.question_2_label.setGeometry(QtCore.QRect(80, 230, 260, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_2_label.setFont(font)
        self.question_2_label.setObjectName("question_2_label")

        #「問題2」下拉式選單
        self.question_2_comboBox = QtWidgets.QComboBox(self.page_7)
        self.question_2_comboBox.setGeometry(QtCore.QRect(340, 230, 181, 26))
        self.question_2_comboBox.setObjectName("question_2_comboBox")
        self.question_2_comboBox.addItem("")
        self.question_2_comboBox.addItem("")
        self.question_2_comboBox.addItem("")
        self.question_2_comboBox.addItem("")
        self.question_2_comboBox.addItem("")
        self.question_2_comboBox.addItem("")
        self.question_2_comboBox.addItem("")

        #「問題3」標籤
        self.question_3_label = QtWidgets.QLabel(self.page_7)
        self.question_3_label.setGeometry(QtCore.QRect(80, 300, 234, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_3_label.setFont(font)
        self.question_3_label.setObjectName("question_3_label")

        #「問題3」下拉式選單
        self.question_3_comboBox = QtWidgets.QComboBox(self.page_7)
        self.question_3_comboBox.setGeometry(QtCore.QRect(340, 300, 181, 26))
        self.question_3_comboBox.setObjectName("question_3_comboBox")
        self.question_3_comboBox.addItem("")
        self.question_3_comboBox.addItem("")
        self.question_3_comboBox.addItem("")
        self.question_3_comboBox.addItem("")
        self.question_3_comboBox.addItem("")
        self.question_3_comboBox.addItem("")

        #「問題4」標籤
        self.question_4_label = QtWidgets.QLabel(self.page_7)
        self.question_4_label.setGeometry(QtCore.QRect(80, 380, 234, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_4_label.setFont(font)
        self.question_4_label.setObjectName("question_4_label")

        #「問題4」下拉式選單
        self.question_4_comboBox = QtWidgets.QComboBox(self.page_7)
        self.question_4_comboBox.setGeometry(QtCore.QRect(340, 380, 181, 26))
        self.question_4_comboBox.setObjectName("question_4_comboBox")
        self.question_4_comboBox.addItem("")
        self.question_4_comboBox.addItem("")
        self.question_4_comboBox.addItem("")

        #「問題5」標籤
        self.question_5_label = QtWidgets.QLabel(self.page_7)
        self.question_5_label.setGeometry(QtCore.QRect(80, 460, 280, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_5_label.setFont(font)
        self.question_5_label.setObjectName("question_5_label")

        #「問題5」是，按鈕
        self.question_5yes_Button = QtWidgets.QRadioButton(self.page_7)
        self.question_5yes_Button.setGeometry(QtCore.QRect(370, 460, 41, 20))
        self.question_5yes_Button.setObjectName("question_5yes_Button")

        #「問題5」否，按鈕
        self.question_5no_Button = QtWidgets.QRadioButton(self.page_7)
        self.question_5no_Button.setGeometry(QtCore.QRect(440, 460, 41, 20))
        self.question_5no_Button.setObjectName("question_5no_Button")

        # 「問題5」總按鈕
        self.question5_group = QtWidgets.QButtonGroup(self.page_7)
        self.question5_group.addButton(self.question_5yes_Button)
        self.question5_group.addButton(self.question_5no_Button)

        #「問題6」標籤
        self.question_6_label = QtWidgets.QLabel(self.page_7)
        self.question_6_label.setGeometry(QtCore.QRect(80, 530, 250, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_6_label.setFont(font)
        self.question_6_label.setObjectName("question_6_label")

        #「問題6」是，按鈕
        self.question_6yes_Button = QtWidgets.QRadioButton(self.page_7)
        self.question_6yes_Button.setGeometry(QtCore.QRect(370, 540, 41, 20))
        self.question_6yes_Button.setObjectName("question_6yes_Button")

        #「問題6」否，按鈕
        self.question_6no_Button = QtWidgets.QRadioButton(self.page_7)
        self.question_6no_Button.setGeometry(QtCore.QRect(440, 540, 41, 20))
        self.question_6no_Button.setObjectName("question_6no_Button")

        # 「問題6」總按鈕
        self.question6_group = QtWidgets.QButtonGroup(self.page_7)
        self.question6_group.addButton(self.question_6yes_Button)
        self.question6_group.addButton(self.question_6no_Button)

        #「問題7」標籤
        self.question_7_label = QtWidgets.QLabel(self.page_7)
        self.question_7_label.setGeometry(QtCore.QRect(570, 160, 310, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_7_label.setFont(font)
        self.question_7_label.setObjectName("question_7_label")

        #「問題8」標籤
        self.question_8_label = QtWidgets.QLabel(self.page_7)
        self.question_8_label.setGeometry(QtCore.QRect(570, 230, 310, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_8_label.setFont(font)
        self.question_8_label.setObjectName("question_8_label")

        #「問題9」標籤
        self.question_9_label = QtWidgets.QLabel(self.page_7)
        self.question_9_label.setGeometry(QtCore.QRect(570, 310, 310, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_9_label.setFont(font)
        self.question_9_label.setObjectName("question_9_label")

        #「問題10」標籤
        self.question_10_label = QtWidgets.QLabel(self.page_7)
        self.question_10_label.setGeometry(QtCore.QRect(570, 380, 310, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_10_label.setFont(font)
        self.question_10_label.setObjectName("question_10_label")

        #「問題11」標籤
        self.question_11_label = QtWidgets.QLabel(self.page_7)
        self.question_11_label.setGeometry(QtCore.QRect(570, 460, 310, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_11_label.setFont(font)
        self.question_11_label.setObjectName("question_11_label")
        
        #點擊程度的上排數字標籤（1到10那個）
        self.eye_situation_upnumber_label_edit = QtWidgets.QLabel(self.page_7)
        self.eye_situation_upnumber_label_edit.setGeometry(QtCore.QRect(882, 145, 200, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.eye_situation_upnumber_label_edit.setFont(font)
        self.eye_situation_upnumber_label_edit.setObjectName("eye_situation_upnumber_label_edit")
             
        # 創建 QButtonGroup 並將按鈕加入組(posttest)
        self.question_button_group7 = QtWidgets.QButtonGroup(self.page_7)# 配戴眼鏡的頻率
        self.question_button_group8 = QtWidgets.QButtonGroup(self.page_7)# 配戴隱眼的頻率
        self.question_button_group9 = QtWidgets.QButtonGroup(self.page_7)# 眼睛乾澀頻率
        self.question_button_group10 = QtWidgets.QButtonGroup(self.page_7)# 頭痛暈眩頻率
        self.question_button_group11 = QtWidgets.QButtonGroup(self.page_7)# 眼睛疲勞頻率
        # 根據提供的 x 座標生成 QRadioButton
        self.temp_button7 = []  
        self.temp_button8 = []  
        self.temp_button9 = []  
        self.temp_button10 = []  
        self.temp_button11 = []  
        x_positions = [880, 899, 918, 937, 957, 977, 996, 1017, 1038, 1060]  
        y_position1 = 160  
        y_position2 = 230  
        y_position3 = 310 
        y_position4 = 380
        y_position5 = 460
        # 配戴眼鏡的頻率（QRadioButton 正確使用）
        for i, x in enumerate(x_positions, 1):  # 根據 x_positions 的位置來生成按鈕
            question_button7 = QtWidgets.QRadioButton(self.page_7)
            question_button7.setGeometry(QtCore.QRect(x, y_position1, 161, 22))
            question_button7.setObjectName(f"question_button7_{i}")
            self.temp_button7.append(question_button7)
            self.question_button_group7.addButton(question_button7, i)  # 將按鈕加入到 ButtonGroup 並指定ID

        # 配戴隱眼的頻率
        for i, x in enumerate(x_positions, 1):  
            question_button8 = QtWidgets.QRadioButton(self.page_7)
            question_button8.setGeometry(QtCore.QRect(x, y_position2, 161, 22))
            question_button8.setObjectName(f"question_button8_{i}")
            self.temp_button8.append(question_button8)
            self.question_button_group8.addButton(question_button8, i)  # 指定ID

        # 眼睛乾澀頻率
        for i, x in enumerate(x_positions, 1):  
            question_button9 = QtWidgets.QRadioButton(self.page_7)
            question_button9.setGeometry(QtCore.QRect(x, y_position3, 161, 22))
            question_button9.setObjectName(f"question_button9_{i}")
            self.temp_button9.append(question_button9)
            self.question_button_group9.addButton(question_button9, i)  # 指定ID

        # 頭痛暈眩頻率
        for i, x in enumerate(x_positions, 1):  
            question_button10 = QtWidgets.QRadioButton(self.page_7)
            question_button10.setGeometry(QtCore.QRect(x, y_position4, 161, 22))
            question_button10.setObjectName(f"question_button10_{i}")
            self.temp_button10.append(question_button10)
            self.question_button_group10.addButton(question_button10, i)  # 指定ID

        # 眼睛疲勞頻率
        for i, x in enumerate(x_positions, 1):  
            question_button11 = QtWidgets.QRadioButton(self.page_7)
            question_button11.setGeometry(QtCore.QRect(x, y_position5, 161, 22))
            question_button11.setObjectName(f"question_button11_{i}")
            self.temp_button11.append(question_button11)
            self.question_button_group11.addButton(question_button11, i)  # 指定ID


        #「問題12」標籤
        self.question_12_label = QtWidgets.QLabel(self.page_7)
        self.question_12_label.setGeometry(QtCore.QRect(570, 540, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.question_12_label.setFont(font)
        self.question_12_label.setObjectName("question_12_label")

        #「問題12」輸入匡
        self.question_12_input = QtWidgets.QLineEdit(self.page_7)
        self.question_12_input.setGeometry(QtCore.QRect(810, 540, 261, 21))
        self.question_12_input.setObjectName("question_12_input")

        #「送出」按鈕（最下面那個）
        self.Sendout_Button = QtWidgets.QPushButton(self.page_7)
        self.Sendout_Button.setGeometry(QtCore.QRect(478, 590, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Sendout_Button.setFont(font)
        self.Sendout_Button.setObjectName("Sendout_Button")


        self.stackedWidget.addWidget(self.page_7)
        
        
        self.page_8 = QtWidgets.QWidget()
        self.page_8.setObjectName("page_8")
        
        # 創建一個 QLabel 用於顯示圖片
        self.secondpage_picture_label_8 = QtWidgets.QLabel(self.page_8)
        self.secondpage_picture_label_8.setGeometry(0, 0, 1108, 670)  # 直接設置尺寸
        self.secondpage_picture_label_8.setScaledContents(True)  # 讓圖片自動縮放
        #self.secondpage_picture_label_8.setPixmap(QtGui.QPixmap(r"C:\Users\Ivan\Downloads\Eye-Myself\底圖_4.png").scaled(1108, 670, QtCore.Qt.IgnoreAspectRatio))
        self.secondpage_picture_label_8.setAlignment(QtCore.Qt.AlignCenter)
        
        #「使用者說明」大標籤
        self.introduction_title_label = QtWidgets.QLabel(self.page_8)
        self.introduction_title_label.setGeometry(QtCore.QRect(415, 25, 291, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.introduction_title_label.setFont(font)
        self.introduction_title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.introduction_title_label.setObjectName("introduction_title_label")
        # 兩條線
        self.line_1 = QtWidgets.QFrame(self.page_8)
        self.line_1.setGeometry(QtCore.QRect(35, 95, 1001, 20))  # 向上10
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")

        self.line_2 = QtWidgets.QFrame(self.page_8)
        self.line_2.setGeometry(QtCore.QRect(35, 525, 1001, 20))  # 向上10
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        # 數字1標籤
        self.number1_label = QtWidgets.QLabel(self.page_8)
        self.number1_label.setGeometry(QtCore.QRect(195, 150, 41, 61))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(30)
        self.number1_label.setFont(font)
        self.number1_label.setObjectName("number1_label")

        # 數字2標籤
        self.number2_label = QtWidgets.QLabel(self.page_8)
        self.number2_label.setGeometry(QtCore.QRect(195, 255, 41, 61))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(30)
        self.number2_label.setFont(font)
        self.number2_label.setObjectName("number2_label")

        # 數字3標籤
        self.number3_label = QtWidgets.QLabel(self.page_8)
        self.number3_label.setGeometry(QtCore.QRect(195, 355, 41, 61))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(30)
        self.number3_label.setFont(font)
        self.number3_label.setObjectName("number3_label")

        # 數字4標籤
        self.number4_label = QtWidgets.QLabel(self.page_8)
        self.number4_label.setGeometry(QtCore.QRect(195, 455, 41, 61))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(30)
        self.number4_label.setFont(font)
        self.number4_label.setObjectName("number4_label")

        # 第一句上行
        self.description1_1_label = QtWidgets.QLabel(self.page_8)
        self.description1_1_label.setGeometry(QtCore.QRect(235, 145, 721, 31))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description1_1_label.setFont(font)
        self.description1_1_label.setObjectName("description1_1_label")

        # 第一句下行
        self.description1_2_label = QtWidgets.QLabel(self.page_8)
        self.description1_2_label.setGeometry(QtCore.QRect(235, 185, 721, 31))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description1_2_label.setFont(font)
        self.description1_2_label.setObjectName("description1_2_label")

        # 第二句上行
        self.description2_1_label = QtWidgets.QLabel(self.page_8)
        self.description2_1_label.setGeometry(QtCore.QRect(235, 255, 731, 20))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description2_1_label.setFont(font)
        self.description2_1_label.setObjectName("description2_1_label")

        # 第二句下行
        self.description2_2_label = QtWidgets.QLabel(self.page_8)
        self.description2_2_label.setGeometry(QtCore.QRect(235, 295, 701, 20))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description2_2_label.setFont(font)
        self.description2_2_label.setObjectName("description2_2_label")

        # 第三句上行
        self.description3_1_label = QtWidgets.QLabel(self.page_8)
        self.description3_1_label.setGeometry(QtCore.QRect(235, 355, 681, 21))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description3_1_label.setFont(font)
        self.description3_1_label.setObjectName("description3_1_label")

        # 第三句下行
        self.description3_2_label = QtWidgets.QLabel(self.page_8)
        self.description3_2_label.setGeometry(QtCore.QRect(235, 395, 671, 21))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description3_2_label.setFont(font)
        self.description3_2_label.setObjectName("description3_2_label")

        # 第四句
        self.description4_1_label = QtWidgets.QLabel(self.page_8)
        self.description4_1_label.setGeometry(QtCore.QRect(235, 475, 681, 21))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description4_1_label.setFont(font)
        self.description4_1_label.setObjectName("description4_1_label")

        # 「送出」按鈕  
        self.introduction_send_pushButton = QtWidgets.QPushButton(self.page_8)
        self.introduction_send_pushButton.setGeometry(QtCore.QRect(465, 605, 181, 31))  # 向上10
        self.introduction_send_pushButton.setObjectName("introduction_send_pushButton")

        # 「我已知悉使用條款」按鈕
        self.introduction_agree_radioButton = QtWidgets.QRadioButton(self.page_8)
        self.introduction_agree_radioButton.setGeometry(QtCore.QRect(425, 565, 281, 20))  # 向上10
        font = QtGui.QFont()
        font.setPointSize(10)
        self.introduction_agree_radioButton.setFont(font)
        self.introduction_agree_radioButton.setObjectName("introduction_agree_radioButton")

        self.stackedWidget.addWidget(self.page_8)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Eye myself"))
        self.login.setText(_translate("MainWindow", "Log in"))
        self.Signup.setText(_translate("MainWindow", "Sign up"))
        self.Edit.setText(_translate("MainWindow", "Edit"))
        self.Analysis.setText(_translate("MainWindow", "Analysis"))
        self.name_label.setText(_translate("MainWindow", "Name"))
        self.open_camera.setText(_translate("MainWindow", "Camera"))
        self.label_2.setText(_translate("MainWindow", "Blink Threshlod"))
        self.label_3.setText(_translate("MainWindow", "Brightness Threshold"))
        self.label_4.setText(_translate("MainWindow", "Distance Threshold"))
        self.blink_num.setText(_translate("MainWindow", "Blink per min"))
        self.label_5.setText(_translate("MainWindow", "Working Time"))
        self.label_6.setText(_translate("MainWindow", "min"))
        self.label_7.setText(_translate("MainWindow", "Resting Time"))
        self.label_8.setText(_translate("MainWindow", "min"))
        self.label_9.setText(_translate("MainWindow", "Exercise Type"))
        self.label_10.setText(_translate("MainWindow", "Number"))
        self.suggestion.setText(_translate("MainWindow", "Suggestion"))
        self.start.setText(_translate("MainWindow", "Start"))
        self.name_label_2.setText(_translate("MainWindow", "Name"))
        self.label_11.setText(_translate("MainWindow", "Brightness Threshold"))
        self.label_12.setText(_translate("MainWindow", "Blink Threshlod"))
        self.label_13.setText(_translate("MainWindow", "Distance Threshold"))
        self.pushButton_sve.setText(_translate("MainWindow", "Save"))
        self.Hour.setText(_translate("MainWindow", "hour"))
        self.Second.setText(_translate("MainWindow", "sec"))
        self.Minute.setText(_translate("MainWindow", "min"))
        self.blink_num_1.setText(_translate("MainWindow","Blink per min"))
        self.pushButton_Exhausted.setText(_translate("MainWindow", "Exhausted"))
        self.toolButton_finish.setText(_translate("MainWindow", "Finish"))
        self.label.setText(_translate("MainWindow", "Analysis"))
        self.send_to_line.setText(_translate("MainWindow", "Send to line"))
        '''self.back_to_home.setText(_translate("MainWindow", "Back"))'''
        self.choose_user.setText(_translate("MainWindow", "Choose user"))
        self.name_label3.setText(_translate("MainWindow", "姓           名"))
        self.sex_man_button.setText(_translate("MainWindow", "男生"))
        self.user_name_label.setText(_translate("MainWindow", "使用者名稱"))
        self.birthday_label.setText(_translate("MainWindow", "生           日"))
        self.sex_label.setText(_translate("MainWindow", "性           別"))
        self.sex_women_button.setText(_translate("MainWindow", "女生"))
        self.line_token_label.setText(_translate("MainWindow", "line  token "))
        self.right_eye_label.setText(_translate("MainWindow", "右眼"))
        self.right_eye_out_button.setText(_translate("MainWindow", "遠視"))
        self.right_eye_in_button.setText(_translate("MainWindow", "近視"))
        self.right_eye_shine_button.setText(_translate("MainWindow", "散光"))
        self.left_eye_label.setText(_translate("MainWindow", "左眼"))
        self.left_eye_out_button.setText(_translate("MainWindow", "遠視"))
        self.left_eye_in_button.setText(_translate("MainWindow", "近視"))
        self.left_eye_shine_button.setText(_translate("MainWindow", "散光"))
        self.eye_situation_upnumber_label.setText(_translate("MainWindow", "1   2   3   4   5   6   7   8   9  10"))
        self.eye_situation_label1.setText(_translate("MainWindow", "使用3C產品配戴「眼鏡」的頻率"))
        self.eye_situation_label2.setText(_translate("MainWindow", "使用3C產品配戴「隱眼」的頻率"))
        self.eye_situation_label4.setText(_translate("MainWindow", "頭痛暈眩頻率"))
        self.eye_situation_label3.setText(_translate("MainWindow", "眼睛乾澀頻率"))
        self.eye_situation_label5.setText(_translate("MainWindow", "眼睛疲勞頻率"))
        self.use_situation_label5.setText(_translate("MainWindow", "工作或學習場所之光線情況"))
        self.use_situation5_combobox.setItemText(0, _translate("MainWindow", "僅室內共用燈光"))
        self.use_situation5_combobox.setItemText(1, _translate("MainWindow", "僅室內專用燈光"))
        self.use_situation5_combobox.setItemText(2, _translate("MainWindow", "室內共用與專用燈光皆有"))
        self.use_situation5_combobox.setItemText(3, _translate("MainWindow", "戶外"))
        self.use_situation5_combobox.setItemText(4, _translate("MainWindow", "光線明顯不足之環境"))
        self.use_situation5_combobox.setItemText(5, _translate("MainWindow", "其他"))
        self.habit_label2.setText(_translate("MainWindow", "定期檢查眼睛的頻率"))
        self.use_situation_no_button1.setText(_translate("MainWindow", "否"))
        self.use_situation_label2.setText(_translate("MainWindow", "每次使用電子設備時間(以長時間活動為主)"))
        self.use_situation_yes_button3.setText(_translate("MainWindow", "是"))
        self.habit_no_button1.setText(_translate("MainWindow", "否"))
        self.habit_yes_button1.setText(_translate("MainWindow", "是"))
        self.use_situation_label3.setText(_translate("MainWindow", "是否有使用眼睛保護設備(防藍光設備軟體)"))
        self.habit_combobox2.setItemText(0, _translate("MainWindow", "無"))
        self.habit_combobox2.setItemText(1, _translate("MainWindow", "半年一次"))
        self.habit_combobox2.setItemText(2, _translate("MainWindow", "一年一次"))
        self.habit_combobox2.setItemText(3, _translate("MainWindow", "更頻繁"))
        self.use_situation_label4.setText(_translate("MainWindow", "使用裝置期間調整螢幕亮度的頻率"))
        self.use_situation4_combobox.setItemText(0, _translate("MainWindow", "電腦自動調整"))
        self.use_situation4_combobox.setItemText(1, _translate("MainWindow", "不常調整"))
        self.use_situation4_combobox.setItemText(2, _translate("MainWindow", "每次使用都會調整"))
        self.use_situation2_combobox.setItemText(0, _translate("MainWindow", "3小時以內"))
        self.use_situation2_combobox.setItemText(1, _translate("MainWindow", "3至6小時"))
        self.use_situation2_combobox.setItemText(2, _translate("MainWindow", "6至9小時"))
        self.use_situation2_combobox.setItemText(3, _translate("MainWindow", "9至12小時"))
        self.use_situation2_combobox.setItemText(4, _translate("MainWindow", "12小時以上"))
        self.use_situation_yes_button1.setText(_translate("MainWindow", "是"))
        self.use_situation_label1.setText(_translate("MainWindow", "工作/學習性質是否需要長時間使用電子產品"))
        self.habit_label1.setText(_translate("MainWindow", "平常是否有在食用戶眼保健食品"))
        self.use_situation_no_button3.setText(_translate("MainWindow", "否"))
        self.habit_label3.setText(_translate("MainWindow", "平均每天睡眠時長為"))
        self.habit_combobox3.setItemText(0, _translate("MainWindow", "低於4小時"))
        self.habit_combobox3.setItemText(1, _translate("MainWindow", "4至6小時"))
        self.habit_combobox3.setItemText(2, _translate("MainWindow", "6至8小時"))
        self.habit_combobox3.setItemText(3, _translate("MainWindow", "高於8小時"))
        self.habit_label4.setText(_translate("MainWindow", "平均每週運動次數為"))
        self.habit_combobox4.setItemText(0, _translate("MainWindow", "0或1次"))
        self.habit_combobox4.setItemText(1, _translate("MainWindow", "2或3次"))
        self.habit_combobox4.setItemText(2, _translate("MainWindow", "4或5次"))
        self.habit_combobox4.setItemText(3, _translate("MainWindow", "6次以上"))
        self.habit_combobox5.setItemText(0, _translate("MainWindow", "無休息"))
        self.habit_combobox5.setItemText(1, _translate("MainWindow", "1小時內"))
        self.habit_combobox5.setItemText(2, _translate("MainWindow", "1至2小時"))
        self.habit_combobox5.setItemText(3, _translate("MainWindow", "2至3小時"))
        self.habit_combobox5.setItemText(4, _translate("MainWindow", "3至4小時"))
        self.habit_combobox5.setItemText(5, _translate("MainWindow", "4至5小時"))
        self.habit_combobox5.setItemText(6, _translate("MainWindow", "5小時以上"))
        self.habit_label5.setText(_translate("MainWindow", "使用電子設備時，通常使用多久會休息"))
        self.habit_label6.setText(_translate("MainWindow", "平均每次休息的持續時間約持續多久"))
        self.habit_combobox6.setItemText(0, _translate("MainWindow", "10分鐘內"))
        self.habit_combobox6.setItemText(1, _translate("MainWindow", "11至30分鐘"))
        self.habit_combobox6.setItemText(2, _translate("MainWindow", "31至60分鐘"))
        self.habit_combobox6.setItemText(3, _translate("MainWindow", "60分鐘以上"))
        self.habit_close_checkbox7.setText(_translate("MainWindow", "閉目養神"))
        self.habit_label7.setText(_translate("MainWindow", "眼睛疲勞時，習慣的休息方式為"))
        self.habit_exercise_checkbox7.setText(_translate("MainWindow", "眼部運動"))
        self.habit_other_checkbox7.setText(_translate("MainWindow", "其他"))
        self.Savefile.setText(_translate("MainWindow", "Save"))
        #以上為註冊介面


        #以下為編輯介面
        self.name_label3_edit.setText(_translate("MainWindow", "姓           名"))
        self.sex_man_button_edit.setText(_translate("MainWindow", "男生"))
        self.user_name_label_edit.setText(_translate("MainWindow", "使用者名稱"))
        self.birthday_label_edit.setText(_translate("MainWindow", "生           日"))
        self.sex_label_edit.setText(_translate("MainWindow", "性           別"))
        self.sex_women_button_edit.setText(_translate("MainWindow", "女生"))
        self.line_token_label_edit.setText(_translate("MainWindow", "line  token"))
        self.right_eye_label_edit.setText(_translate("MainWindow", "右眼"))
        self.right_eye_out_button_edit.setText(_translate("MainWindow", "遠視"))
        self.right_eye_in_button_edit.setText(_translate("MainWindow", "近視"))
        self.right_eye_shine_button_edit.setText(_translate("MainWindow", "散光"))
        self.left_eye_label_edit.setText(_translate("MainWindow", "左眼"))
        self.left_eye_out_button_edit.setText(_translate("MainWindow", "遠視"))
        self.left_eye_in_button_edit.setText(_translate("MainWindow", "近視"))
        self.left_eye_shine_button_edit.setText(_translate("MainWindow", "散光"))
        self.eye_situation_label1_edit.setText(_translate("MainWindow", "使用3C產品配戴「眼鏡」的頻率"))
        self.eye_situation_label2_edit.setText(_translate("MainWindow", "使用3C產品配戴「隱眼」的頻率"))
        self.eye_situation_label4_edit.setText(_translate("MainWindow", "頭痛暈眩頻率"))
        self.eye_situation_label3_edit.setText(_translate("MainWindow", "眼睛乾澀頻率"))
        self.eye_situation_label5_edit.setText(_translate("MainWindow", "眼睛疲勞頻率"))
        self.use_situation_label5_edit.setText(_translate("MainWindow", "工作或學習場所之光線情況"))
        self.use_situation5_combobox_edit.setItemText(0, _translate("MainWindow", "僅室內共用燈光"))
        self.use_situation5_combobox_edit.setItemText(1, _translate("MainWindow", "僅室內專用燈光"))
        self.use_situation5_combobox_edit.setItemText(2, _translate("MainWindow", "室內共用與專用燈光皆有"))
        self.use_situation5_combobox_edit.setItemText(3, _translate("MainWindow", "戶外"))
        self.use_situation5_combobox_edit.setItemText(4, _translate("MainWindow", "光線明顯不足之環境"))
        self.use_situation5_combobox_edit.setItemText(5, _translate("MainWindow", "其他"))    
        self.habit_label2_edit.setText(_translate("MainWindow", "定期檢查眼睛的頻率"))
        self.use_situation_no_button1_edit.setText(_translate("MainWindow", "否"))
        self.use_situation_label2_edit.setText(_translate("MainWindow", "每次使用電子設備時間(以長時間活動為主)"))
        self.use_situation_yes_button3_edit.setText(_translate("MainWindow", "是"))
        self.habit_no_button1_edit.setText(_translate("MainWindow", "否"))
        self.habit_yes_button1_edit.setText(_translate("MainWindow", "是"))
        self.use_situation_label3_edit.setText(_translate("MainWindow", "是否有使用眼睛保護設備(防藍光設備軟體)"))
        self.habit_combobox2_edit.setItemText(0, _translate("MainWindow", "無"))
        self.habit_combobox2_edit.setItemText(1, _translate("MainWindow", "半年一次"))
        self.habit_combobox2_edit.setItemText(2, _translate("MainWindow", "一年一次"))
        self.habit_combobox2_edit.setItemText(3, _translate("MainWindow", "更頻繁"))
        self.use_situation_label4_edit.setText(_translate("MainWindow", "使用裝置期間調整螢幕亮度的頻率"))
        self.use_situation4_combobox_edit.setItemText(0, _translate("MainWindow", "電腦自動調整"))
        self.use_situation4_combobox_edit.setItemText(1, _translate("MainWindow", "不常調整"))
        self.use_situation4_combobox_edit.setItemText(2, _translate("MainWindow", "每次使用都會調整"))
        self.use_situation2_combobox_edit.setItemText(0, _translate("MainWindow", "3小時以內"))
        self.use_situation2_combobox_edit.setItemText(1, _translate("MainWindow", "3至6小時"))
        self.use_situation2_combobox_edit.setItemText(2, _translate("MainWindow", "6至9小時"))
        self.use_situation2_combobox_edit.setItemText(3, _translate("MainWindow", "9至12小時"))
        self.use_situation2_combobox_edit.setItemText(4, _translate("MainWindow", "12小時以上"))
        self.use_situation_yes_button1_edit.setText(_translate("MainWindow", "是"))
        self.use_situation_label1_edit.setText(_translate("MainWindow", "工作/學習性質是否需要長時間使用電子產品"))
        self.habit_label1_edit.setText(_translate("MainWindow", "平常是否有在食用戶眼保健食品"))
        self.use_situation_no_button3_edit.setText(_translate("MainWindow", "否"))
        self.habit_label3_edit.setText(_translate("MainWindow", "平均每天睡眠時長為"))
        self.habit_combobox3_edit.setItemText(0, _translate("MainWindow", "低於4小時"))
        self.habit_combobox3_edit.setItemText(1, _translate("MainWindow", "4至6小時"))
        self.habit_combobox3_edit.setItemText(2, _translate("MainWindow", "6至8小時"))
        self.habit_combobox3_edit.setItemText(3, _translate("MainWindow", "高於8小時"))
        self.habit_label4_edit.setText(_translate("MainWindow", "平均每週運動次數為"))
        self.habit_combobox4_edit.setItemText(0, _translate("MainWindow", "0或1次"))
        self.habit_combobox4_edit.setItemText(1, _translate("MainWindow", "2或3次"))
        self.habit_combobox4_edit.setItemText(2, _translate("MainWindow", "4或5次"))
        self.habit_combobox4_edit.setItemText(3, _translate("MainWindow", "6次以上"))
        self.habit_combobox5_edit.setItemText(0, _translate("MainWindow", "無休息"))
        self.habit_combobox5_edit.setItemText(1, _translate("MainWindow", "1小時內"))
        self.habit_combobox5_edit.setItemText(2, _translate("MainWindow", "1至2小時"))
        self.habit_combobox5_edit.setItemText(3, _translate("MainWindow", "2至3小時"))
        self.habit_combobox5_edit.setItemText(4, _translate("MainWindow", "3至4小時"))
        self.habit_combobox5_edit.setItemText(5, _translate("MainWindow", "4至5小時"))
        self.habit_combobox5_edit.setItemText(6, _translate("MainWindow", "5小時以上"))
        self.habit_label5_edit.setText(_translate("MainWindow", "使用電子設備時，通常使用多久會休息"))
        self.habit_label6_edit.setText(_translate("MainWindow", "平均每次休息的持續時間約持續多久"))
        self.habit_combobox6_edit.setItemText(0, _translate("MainWindow", "10分鐘內"))
        self.habit_combobox6_edit.setItemText(1, _translate("MainWindow", "11至30分鐘"))
        self.habit_combobox6_edit.setItemText(2, _translate("MainWindow", "31至60分鐘"))
        self.habit_combobox6_edit.setItemText(3, _translate("MainWindow", "60分鐘以上"))
        self.habit_close_checkbox7_edit.setText(_translate("MainWindow", "閉目養神"))
        self.habit_label7_edit.setText(_translate("MainWindow", "眼睛疲勞時，習慣的休息方式為"))
        self.habit_exercise_checkbox7_edit.setText(_translate("MainWindow", "眼部運動"))
        self.habit_other_checkbox7_edit.setText(_translate("MainWindow", "其他"))
        self.Savefile_edit.setText(_translate("MainWindow", "Save"))
        self.deletefile_edit.setText(_translate("MainWindow", "刪除"))
        self.eye_situation_upnumber_label_edit.setText(_translate("MainWindow", "1   2   3   4   5   6   7   8   9  10"))


        self.Sendout_Button.setText(_translate("MainWindow", "送出"))
        self.top_label.setText(_translate("MainWindow", "本問卷旨在了解您在使用電子產品時的用眼狀況，以便我們的系統能夠更好地為您提供客製化的用眼健康提醒。\n"
"我們希望通過這些數據來改善您在使用電子產品過程中的視覺舒適度，並減少眼部疲勞。\n"
"請根據您的實際體感回答以下問題。我們承諾所有的數據將僅用於本次研究，並會嚴格保密。謝謝您的合作！"))
        self.question_1_comboBox.setItemText(0, _translate("MainWindow", "電腦"))
        self.question_1_comboBox.setItemText(1, _translate("MainWindow", "手機"))
        self.question_1_comboBox.setItemText(2, _translate("MainWindow", "平板"))
        self.question_1_comboBox.setItemText(3, _translate("MainWindow", "其他"))
        self.question_2_comboBox.setItemText(0, _translate("MainWindow", "工作/實習用途"))
        self.question_2_comboBox.setItemText(1, _translate("MainWindow", "聆聽線上課程"))
        self.question_2_comboBox.setItemText(2, _translate("MainWindow", "完成學校作業"))
        self.question_2_comboBox.setItemText(3, _translate("MainWindow", "打電腦遊戲"))
        self.question_2_comboBox.setItemText(4, _translate("MainWindow", "觀看影音串流平台(如Youtube)"))
        self.question_2_comboBox.setItemText(5, _translate("MainWindow", "回覆訊息文字"))
        self.question_2_comboBox.setItemText(6, _translate("MainWindow", "其他"))
        self.question_5yes_Button.setText(_translate("MainWindow", "是"))
        self.question_5no_Button.setText(_translate("MainWindow", "否"))
        self.question_6yes_Button.setText(_translate("MainWindow", "是"))
        self.question_6no_Button.setText(_translate("MainWindow", "否"))
        self.question_4_comboBox.setItemText(0, _translate("MainWindow", "無"))
        self.question_4_comboBox.setItemText(1, _translate("MainWindow", "配戴眼鏡"))
        self.question_4_comboBox.setItemText(2, _translate("MainWindow", "配戴隱形眼鏡"))
        self.question_3_comboBox.setItemText(0, _translate("MainWindow", "僅室內共用燈光"))
        self.question_3_comboBox.setItemText(1, _translate("MainWindow", "僅室內專用燈光"))
        self.question_3_comboBox.setItemText(2, _translate("MainWindow", "室內共用與專用燈光皆有"))
        self.question_3_comboBox.setItemText(3, _translate("MainWindow", "戶外"))
        self.question_3_comboBox.setItemText(4, _translate("MainWindow", "光線明顯不足之環境"))
        self.question_3_comboBox.setItemText(5, _translate("MainWindow", "其他"))
        self.question_1_label.setText(_translate("MainWindow", "此次施策時使用的電子產品為"))
        self.question_2_label.setText(_translate("MainWindow", "此次使用該電子產品的主要用途為"))
        self.question_3_label.setText(_translate("MainWindow", "此次紀錄時的環境光線使用為"))
        self.question_4_label.setText(_translate("MainWindow", "此次紀錄時是否有配戴眼鏡類產品"))
        self.question_6_label.setText(_translate("MainWindow", "此次紀錄是否有使用電腦增高架"))
        self.question_5_label.setText(_translate("MainWindow", "此次紀錄是否有產生眼睛疲勞等症狀"))
        self.question_7_label.setText(_translate("MainWindow", "使用本系統後，眼睛疲勞程度是否有改善"))
        self.question_8_label.setText(_translate("MainWindow", "此次紀錄時，關於\"眨眼\"的提醒是否準確"))
        self.question_9_label.setText(_translate("MainWindow", "此次紀錄時，關於\"距離\"的提醒是否準確"))
        self.question_12_label.setText(_translate("MainWindow", "備註/問題/是否有其他變因"))
        self.question_11_label.setText(_translate("MainWindow", "此次紀錄時，關於\"休息\"的提醒是否準確"))
        self.question_10_label.setText(_translate("MainWindow", "此次紀錄時，關於\"亮度\"的提醒是否準確"))
        #以下為page_8，使用者說明同意介面
        self.description1_1_label.setText(_translate("MainWindow", "本系統將收集並分析使用者的基本資料及用眼數據，該數據僅用於學術研究及系統優化。"))
        self.description3_2_label.setText(_translate("MainWindow", "這將有助於我們進一步優化系統，提供更精確的健康建議。"))
        self.description2_1_label.setText(_translate("MainWindow", "本系統所提供的用眼建議與提醒僅供參考，旨在協助使用者改善用眼習慣，並減少眼睛疲勞。"))
        self.description1_2_label.setText(_translate("MainWindow", "所有收集的個人資料將受到嚴格保密，並不會用於其他商業目的或外洩。"))
        self.number1_label.setText(_translate("MainWindow", "1."))
        self.introduction_title_label.setText(_translate("MainWindow", "使用者說明"))
        self.number2_label.setText(_translate("MainWindow", "2."))
        self.number3_label.setText(_translate("MainWindow", "3."))
        self.description2_2_label.setText(_translate("MainWindow", "對於任何嚴重的眼部健康問題，請務必諮詢專業醫療人員。"))
        self.description3_1_label.setText(_translate("MainWindow", "每次測試結束後，請務必填寫系統提供的簡易問卷，以回饋您的用眼感受及身體狀況。"))
        self.introduction_send_pushButton.setText(_translate("MainWindow", "送出"))
        self.number4_label.setText(_translate("MainWindow", "4."))
        self.description4_1_label.setText(_translate("MainWindow", "測驗期間，請確保網路連接順暢，以避免數據上傳失敗。"))
        self.introduction_agree_radioButton.setText(_translate("MainWindow", "本人已閱讀並同意相關服務條款"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
