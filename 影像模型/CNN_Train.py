import torch
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import clip
import torch.nn as nn
import torch.nn.functional as F
import os

# 設置設備
device = "cuda" if torch.cuda.is_available() else "cpu"

# 定義 CNN 模型結構
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

# 定義 CLIP + CNN + FCNN 模型
class CLIP_CNN_FCNN(nn.Module):
    def __init__(self, clip_feature_dim, cnn_feature_dim, num_classes=2):
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

# 提取 CLIP 第一層和最後一層特徵
def get_clip_features(model, image):
    features = {}

    def hook_fn(module, input, output):
        features[module] = output

    first_layer_hook = model.visual.conv1.register_forward_hook(hook_fn)
    last_layer_hook = model.visual.transformer.resblocks[-1].register_forward_hook(hook_fn)

    with torch.no_grad():
        model.encode_image(image)

    first_layer_hook.remove()
    last_layer_hook.remove()

    return features[model.visual.conv1], features[model.visual.transformer.resblocks[-1]]

# 定義數據集
class ImageDataset(Dataset):
    def __init__(self, image_folder, label, clip_model, preprocess, cnn_model):
        self.image_paths = [os.path.join(image_folder, fname) for fname in os.listdir(image_folder) if fname.endswith((".jpg", ".png"))]
        self.label = label
        self.clip_model = clip_model
        self.preprocess = preprocess
        self.cnn_model = cnn_model

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        img = Image.open(image_path).resize((224, 224))
        image_tensor = self.preprocess(img).unsqueeze(0).to(device)

        # 提取 CLIP 特徵
        first_clip_features, last_clip_features = get_clip_features(self.clip_model, image_tensor)
        clip_features = torch.cat([first_clip_features.flatten(1), last_clip_features.flatten(1)], dim=1).squeeze(0)

        # 提取 CNN 特徵
        cnn_features = self.cnn_model(image_tensor).squeeze(0)

        return torch.cat((clip_features, cnn_features)), self.label

# 加載 CLIP 模型和預處理
clip_model, preprocess = clip.load("ViT-B/32", device=device)
clip_model.eval()

# 初始化 CNN 模型
cnn_model = EyeCNN().to(device)
cnn_model.eval()

# 定義數據集
normal_dataset = ImageDataset("/Volumes/Wyvo_FUJITS/nmr", label=0, clip_model=clip_model, preprocess=preprocess, cnn_model=cnn_model)
fatigued_dataset = ImageDataset("/Volumes/Wyvo_FUJITS/exh/eexh", label=1, clip_model=clip_model, preprocess=preprocess, cnn_model=cnn_model)

# 合併數據集
from torch.utils.data import random_split
from torch.utils.data import DataLoader
dataset = normal_dataset + fatigued_dataset
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# 初始化模型
clip_feature_dim = 768 + 512  # 第一層 + 最後一層 CLIP 特徵
cnn_feature_dim = cnn_model.feature_dim
model = CLIP_CNN_FCNN(clip_feature_dim, cnn_feature_dim, num_classes=2).to(device)

# 定義損失函數和優化器
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 開始訓練
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    for features, labels in train_loader:
        features, labels = features.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(features[:, :clip_feature_dim], features[:, clip_feature_dim:])
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

# 保存模型
torch.save(model, "model1228.pth")
print("模型已保存為 model1228.pth")

# 測試模型
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for features, labels in test_loader:
        features, labels = features.to(device), labels.to(device)
        outputs = model(features[:, :clip_feature_dim], features[:, clip_feature_dim:])
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"測試準確率: {100 * correct / total:.2f}%")

# 測試圖片路徑
def classify_image(image_path):
    print(f"分類圖片：{image_path}")

    # 確認圖片是否存在
    if not os.path.exists(image_path):
        print(f"圖片路徑無效: {image_path}")
        return None

    # 加載並處理圖片
    img = Image.open(image_path).resize((224, 224))
    image_tensor = preprocess(img).unsqueeze(0).to(device)

    # 提取 CLIP 特徵
    first_clip_features, last_clip_features = get_clip_features(clip_model, image_tensor)
    clip_features = torch.cat([first_clip_features.flatten(1), last_clip_features.flatten(1)], dim=1)

    # 提取 CNN 特徵
    cnn_features = cnn_model(image_tensor)

    # 使用模型分類
    with torch.no_grad():
        outputs = model(clip_features, cnn_features)
        _, predicted = torch.max(outputs, 1)
        return predicted.item()

# 測試圖片路徑
test_image_path = "/Volumes/Wyvo_FUJITS/normalm/20241124-190508-289_camera.jpg"  # 替換為您的測試圖片路徑
result = classify_image(test_image_path)
if result is not None:
    print(f"測試結果：{result} (0=正常, 1=疲勞)")
