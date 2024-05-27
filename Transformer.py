import torch
from torch import nn
from torch.optim import Adam
import math
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import DataLoader, TensorDataset
from torch.optim.lr_scheduler import StepLR
import pandas as pd
from sklearn.model_selection import train_test_split

# 加载数据集
data = pd.read_csv('../dataset/output.csv',encoding = 'gbk')

data = data.drop(data.columns[[0,1, 2, 3, 5]], axis=1)

X = data.iloc[:, 1:]

middle = X.shape[1] // 2
X.insert(middle, 'duplicate_feature', X.iloc[:, 0])

from sklearn.preprocessing import LabelEncoder

X = X.fillna(X.mean())
y = data.iloc[:, 0]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 定义模型
class TransformerModel(nn.Module):
    def __init__(self, input_dim, output_dim, nhead, nhid, nlayers, dropout=0.5):
        super(TransformerModel, self).__init__()
        self.model_type = 'Transformer'
        self.src_mask = None
        self.pos_encoder = PositionalEncoding(input_dim, dropout)
        encoder_layers = nn.TransformerEncoderLayer(input_dim, nhead, nhid, dropout)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, nlayers)
        self.encoder = nn.Linear(input_dim, input_dim)
        self.decoder = nn.Linear(input_dim, output_dim)
        self.init_weights()

    def _generate_square_subsequent_mask(self, sz):
        mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        return mask

    def init_weights(self):
        initrange = 0.1
        self.encoder.bias.data.zero_()
        self.encoder.weight.data.uniform_(-initrange, initrange)
        self.decoder.bias.data.zero_()
        self.decoder.weight.data.uniform_(-initrange, initrange)

    def forward(self, src):
        if self.src_mask is None or self.src_mask.size(0) != len(src):
            device = src.device
            mask = self._generate_square_subsequent_mask(len(src)).to(device)
            self.src_mask = mask

        src = self.encoder(src)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src, self.src_mask)

        # 取第一个位置的向量来代表整个序列
        output = output[0]

        output = self.decoder(output)
        return output

# 定义位置编码
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=X.shape[0]):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return self.dropout(x)

# 参数设置
input_dim = X.shape[1]  # 输入维度
output_dim = len(y.unique())  # 输出维度
nhead = 6  # 多头注意力模型的头数
nhid = 200  # 隐藏层维度
nlayers = 2  # transformer编码器中子编码器层的数量
dropout = 0.2  # dropout值
epoch_num = 101
lr = 0.01  # 初始学习率
step_size = 50  # 学习率调整步长
gamma = 0.1  # 学习率调整因子
batch_size = 128

# 初始化模型
model = TransformerModel(input_dim, output_dim, nhead, nhid, nlayers, dropout)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = Adam(model.parameters())
# 定义学习率调度器
scheduler = StepLR(optimizer, step_size=step_size, gamma=gamma)

# 检查是否有可用的 GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 将类别标签编码为整数
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 将数据转移到 GPU
X_train = torch.from_numpy(X_train.values).float().to(device)
y_train = torch.from_numpy(y_train).long().to(device)  # y_train 现在是整数
X_test_tensor = torch.from_numpy(X_test.values).float().to(device)
y_test_tensor = torch.from_numpy(y_test).long().to(device)  # y_test 现在是整数
# 将模型转移到 GPU
model = model.to(device)

# 创建一个数据集
dataset = TensorDataset(X_train, y_train)

# 定义一个数据加载器，并设置批次大小
batch_size = 64
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# 训练模型
for epoch in range(epoch_num):  # 迭代次数
    model.train()
    for X_batch, y_batch in dataloader:
        optimizer.zero_grad()
        output = model(X_batch)
        loss = criterion(output, y_batch)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        output = model(X_test_tensor)
        predicted = torch.argmax(output, dim=1)
        correct = (predicted == y_test_tensor).sum().item()
        total = y_test_tensor.size(0)
        accuracy = correct / total

    # 更新学习率
    scheduler.step()
    if epoch % 10 == 0:
        print(f'Epoch: {epoch}, Loss: {loss.item()}, Accuracy: {accuracy * 100}%')