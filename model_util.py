import torch
import torch.nn as nn
import torch.nn.functional as F

# MLP模型定义
class MLP(nn.Module):
    def __init__(self, input_size):
        super(MLP, self).__init__()
        self.layer1 = nn.Linear(input_size, 64)
        self.layer2 = nn.Linear(64, 32)
        self.output = nn.Linear(32, 2)  # 二分类任务

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = self.output(x)
        return x


class Predictor:
    def __init__(self, input_size=366, pth_path="mlp_model.pth"):
        self.model = MLP(input_size)
        self.checkpoint = torch.load(pth_path)
        self.model.load_state_dict(self.checkpoint['model_state_dict'])
        self.scaler = self.checkpoint['scaler']
        self.model.eval()

    def predict(self, sample):
        with torch.no_grad():
            sample = self.scaler.transform([sample])
            sample = torch.tensor(sample, dtype=torch.float32)
            output = self.model(sample)
            predicted_class = torch.argmax(output, dim=1).item()
        return predicted_class
