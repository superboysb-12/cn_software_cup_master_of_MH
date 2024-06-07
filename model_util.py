import torch
import torch.nn as nn

# MLP Model Definition
class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

class predictor():
    def __init__(self, pth_path="checkpoint_epoch_100.pth"):
        self.model = MLP(365, 50, 2)
        self.checkpoint = torch.load(pth_path)
        self.model.load_state_dict(self.checkpoint['model_state_dict'])


    def predict(self,sample):
        with torch.no_grad():
            sample = sample.iloc[:, [2] + list(range(6, sample.shape[1] - 1))].values
            sample = torch.tensor(sample, dtype=torch.float32)
            output = self.model(sample)
            predicted_class = torch.argmax(output).item()
        return predicted_class


