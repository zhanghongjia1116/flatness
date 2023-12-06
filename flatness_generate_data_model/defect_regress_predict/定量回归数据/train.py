import numpy as np
import pandas as pd
import torch.optim as optim
from joblib import load as joblib_load
from matplotlib import pyplot as plt
from torch import device as torch_device
from torch import relu, tensor, float32, cuda, save, load
from torch.nn import Module, Linear, MSELoss, RNN
from torch.utils.data import Dataset, DataLoader

feature = ['RCH2: Wedge passline deviation', 'RCH3: Wedge passline deviation',
           'RCH4: Wedge passline deviation',
           'RCH5: Wedge passline deviation', 'F5 ref tension after stand 5',
           'F5 actual value after stand 5 smoothed', 'F5 flatness error tilt',
           'F5  flatness error WR-bend',
           'F5  flatness error IR-bend', 'F5 flatness error', 'F5  flatness error IR-shift',
           'F5 add tilt',
           'F5 add WR-bend',
           'F5 add IR-bend', 'F5 add IR-shift', 'F5 strip length', 'F5 emulsion flow',
           'F5 release tilt control', 'F5 tilt control active', 'F5 release WR-bend control',
           'F5 WR-bend control active', 'F5 release IR-bend control', 'F5 IR-bend control active',
           'F5 release IR-shifting control', 'F5 IR-shifting control active',
           'F5 IR-bending control active MONI',
           'F5 IR-shifting control active MONI', 'STAND_01_reduction', 'STAND_02_reduction',
           'STAND_03_reduction',
           'STAND_04_reduction', 'STAND_05_reduction', 'THC: h ref. S1 entry(ims)',
           'THC: h ref. S1 exit(ims)',
           'THC: act. thickness S1 entry', 'THC: act. thickness S1 exit', 'THX: h ref S5 exit',
           'THX: h act S5 exit', 'SLC laser speed behind S1', 'SLC laser speed behind S4',
           'SLC laser speed behind S5', 'SLC act. speed exit flatness roll', 'SLC act. speed stand 1',
           'SLC act. speed stand 2', 'SLC act. speed stand 3', 'SLC act speed stand 4',
           'SLC act.speed stand 5',
           'SLC strip speed S1 - S2', 'SLC strip speed S2 - S3', 'SLC strip speed S3 - S4',
           'SLC strip speed S4 - S5', 'SLC strip speed after S5', 'SLC Slip factor stand 1',
           'SLC Slip factor stand 2', 'SLC Slip factor stand 3', 'SLC Slip factor stand 4',
           'SLC Slip factor stand 5', 'N1 ITC tension ref value', 'N1 ITC tension actual value DS',
           'N1 ITC tension actual value OS', 'N1 ITC tension actual value at ctrl',
           'N1 ITC diff.tension at ctrl',
           'N2 ITC tension ref value', 'N2 ITC tension actual value DS',
           'N2 ITC tension actual value OS',
           'N2 ITC tension actual value at ctrl', 'N2 ITC diff.tension at ctrl',
           'N3 ITC tension ref value',
           'N3 ITC tension actual value DS', 'N3 ITC tension actual value OS',
           'N3 ITC tension actual value at ctrl', 'N3 ITC diff.tension at ctrl',
           'N4 ITC tension ref value',
           'N4 ITC tension actual value DS', 'N4 ITC tension actual value OS',
           'N4 ITC tension actual value at ctrl', 'N4 ITC diff.tension at ctrl',
           'N5 ITC tension ref value',
           'N5 ITC tension actual value DS', 'N5 ITC tension actual value OS',
           'N5 ITC tension actual value at ctrl', 'N5 ITC diff.tension at ctrl',
           'N5 tension actual value DS after S5', 'N5 tension actual value OS after S5',
           'D1 XSS position actual value', 'D1 WSS position ref value',
           'D1 XFR roll force actual value',
           'D1 WFR roll force ref value', 'D1 XSSd tilting actual value', 'D1 WSSd tilting ref value',
           'D1 DIFF RF CTRL act value (DS-OS)', 'D2 XSS position actual value',
           'D2 WSS position ref value',
           'D2 XFR roll force actual value', 'D2 WFR roll force ref value',
           'D2 XSSd tilting actual value',
           'D2 WSSd tilting ref value', 'D2 DIFF RF CTRL act value (DS-OS)',
           'D3 XSS position actual value',
           'D3 WSS position ref value', 'D3 XFR roll force actual value', 'D3 WFR roll force ref value',
           'D3 XSSd tilting actual value', 'D3 WSSd tilting ref value',
           'D3 DIFF RF CTRL act value (DS-OS)',
           'D4 XSS position actual value', 'D4 WSS position ref value',
           'D4 XFR roll force actual value',
           'D4 WFR roll force ref value', 'D4 XSSd tilting actual value', 'D4 WSSd tilting ref value',
           'D4 DIFF RF CTRL act value (DS-OS)', 'D5 XSS position actual value',
           'D5 WSS position ref value',
           'D5 XFR roll force actual value', 'D5 WFR roll force ref value',
           'D5 XSSd tilting actual value',
           'D5 WSSd tilting ref value', 'D5 DIFF RF CTRL act value (DS-OS)', 'B1 BURB actual value',
           'B1 BURB ref value', 'B1 WRB actual value', 'B1 WRB ref value', 'B1 IRB ref value',
           'B1 IRB ref value ctrl1', 'B1 IRB actual value ctrl1', 'B1 IRB ref value ctrl2',
           'B1 IRB actual value ctrl2', 'B2 BURB actual value', 'B2 BURB ref value',
           'B2 WRB actual value',
           'B2 WRB ref value', 'B2 IRB ref value', 'B2 IRB ref value ctrl1',
           'B2 IRB actual value ctrl1',
           'B2 IRB ref value ctrl2', 'B2 IRB actual value ctrl2', 'B3 BURB actual value',
           'B3 BURB ref value',
           'B3 WRB actual value', 'B3 WRB ref value', 'B3 IRB ref value', 'B3 IRB ref value ctrl1',
           'B3 IRB actual value ctrl1', 'B3 IRB ref value ctrl2', 'B3 IRB actual value ctrl2',
           'WR bending actual value', 'B4 IRB ref value', 'B4 IRB ref value ctrl1',
           'B4 IRB actual value ctrl1',
           'B4 IRB ref value ctrl2', 'B4 IRB actual value ctrl2', 'B5 BURB actual value',
           'B5 WRB actual value',
           'B5 WRB ref value', 'B5 IRB ref value', 'B5 IRB ref value ctrl1',
           'B5 IRB actual value ctrl1',
           'B5 IRB ref value ctrl2', 'B5 IRB actual value ctrl2', 'S1 top IR shfiting ref value',
           'S1 top IR shfitingl actual value', 'S1 bot IR shfiting ref value',
           'S1 bot IR shfitingl actual value',
           'S1 ref value level 2', 'S2 top IR shfiting ref value', 'S2 top IR shfiting actual value',
           'S2 bot IR shfiting ref value', 'S2 bot IR shfiting actual value', 'S2 ref value level 2',
           'S3 top IR shfitingl ref value', 'S3 top IR shfiting actual value',
           'S3 bot IR shfiting ref value',
           'S3 bot IR shfiting actual value', 'S3 ref value level 2', 'S4 top  IR shfiting  ref value',
           'S4 top  IR shfiting actual value', 'S4 bot IR shfiting ref value',
           'S4 bot IR shfiting actual value',
           'S4 ref value level 2', 'S5 top IR shfiting ref value', 'S5 top IR shfiting actual value',
           'S5 bot IR shfiting ref value', 'S5 bot IR shfiting actual value', 'S5 ref value level 2',
           'S2 FLOW',
           'S3 FLOW', 'T3 TEMP.', 'T3 LEV.', 'RCH1: Wedge passline deviation', 'POS', 'deg0', 'deg1',
           'deg2',
           'deg3', 'deg4']


class MyDataset(Dataset):
    def __init__(self, features, targets):
        self.features = tensor(features, dtype=float32)
        self.targets = tensor(targets, dtype=float32)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, index):
        return self.features[index], self.targets[index]


class MLP(Module):
    def __init__(self, input_size, output_size):
        super(MLP, self).__init__()
        self.fc1 = Linear(input_size, 64)  # 64个神经元
        self.fc2 = Linear(64, 32)  # 32个神经元
        self.fc3 = Linear(32, output_size)  # 输出层

    def forward(self, x):
        x = relu(self.fc1(x))
        x = relu(self.fc2(x))
        x = self.fc3(x)
        return x


# 创建循环神经网络模型
class RNN_model(Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN_model, self).__init__()
        self.rnn = RNN(input_size, hidden_size, batch_first=True)
        self.fc = Linear(hidden_size, output_size)

    def forward(self, x):
        # 确保RNN层返回整个序列
        out, _ = self.rnn(x)
        # 使用最后一个时间步的输出
        out = self.fc(out[:, -1, :])
        return out


# 形成训练数据，例如12345789 12-3、23-4、34-5
def split_data(data, timestep, input_size):
    dataX = []  # 保存X
    dataY = []  # 保存Y

    # 将整个窗口的数据保存到X中，将未来一天保存到Y中
    for index in range(len(data) - timestep):
        dataX.append(data[index: index + timestep][:, 0])
        dataY.append(data[index + timestep][0])

    dataX = np.array(dataX)
    dataY = np.array(dataY)

    # 获取训练集大小
    train_size = int(np.round(0.8 * dataX.shape[0]))

    # 划分训练集、测试集
    x_train = dataX[: train_size, :].reshape(-1, timestep, input_size)
    y_train = dataY[: train_size].reshape(-1, 1)

    x_test = dataX[train_size:, :].reshape(-1, timestep, input_size)
    y_test = dataY[train_size:].reshape(-1, 1)

    return [x_train, y_train, x_test, y_test]


def train_BP():
    train_data = pd.read_pickle('train_data.pkl')
    train_data = train_data[feature]

    # 提取特征和目标列
    features = train_data.values  # 前面所有列除了最后5列
    targets = train_data.iloc[:, -5:].values  # 最后5列

    # 标准化特征
    scalerX = joblib_load(rf'standardScalerX.m')
    scalerY = joblib_load(rf'standardScalerY.m')
    x = scalerX.transform(features)
    y = scalerY.transform(targets)

    # 实例化模型和定义损失函数与优化器：
    input_size = len(feature)
    output_size = 5
    model = MLP(input_size, output_size)
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 将模型移动到GPU上
    device = torch_device('cuda' if cuda.is_available() else 'cpu')
    model = model.to(device)

    criterion = MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    num_epochs = 50
    batch_size = 64

    train_dataset = MyDataset(x, y)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(num_epochs):
        for inputs, labels in train_loader:
            # 将每个batch的输入和标签移到GPU上
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

    # 保存模型
    save({
        'epoch': num_epochs,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss.item(),
    }, 'BPmodel.pth')


def predict_BP():
    # 加载PyTorch模型
    input_size = len(feature)
    output_size = 5
    model = MLP(input_size, output_size)
    checkpoint = load('BPmodel.pth')
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()

    predict_data = pd.read_csv(r'H119B21901000_1.csv', usecols=feature, encoding='gbk').dropna().reset_index(drop=True)
    predict_x = predict_data.values
    actual_y = predict_data.iloc[:, -5:].values

    # 标准化特征
    scalerX = joblib_load(rf'standardScalerX.m')
    scalerY = joblib_load(rf'standardScalerY.m')
    predict_x = scalerX.transform(predict_x)

    predict_x = tensor(predict_x, dtype=float32)
    # predict_x = predict_x.reshape(-1, 1, input_size)
    predict_y = model(predict_x)
    predict_y = predict_y.detach().numpy()
    predict_y = scalerY.inverse_transform(predict_y)
    # predict = predict.reshape(-1, output_size)
    predict_y = pd.DataFrame(predict_y, columns=['deg 0', 'deg 1',
                                                 'deg 2', 'deg 3',
                                                 'deg 4'])
    # 绘制实际值与预测值的图像
    plt.figure(figsize=(10, 6), dpi=200)

    for i in range(actual_y.shape[1]):
        plt.plot(actual_y[:, i], label=f'Actual {i + 1}')
        plt.plot(predict_y.iloc[:, i], linestyle='--', label=f'Predicted {i + 1}')
        plt.xlabel('Sample Index')
        plt.ylabel('Values')
        plt.title('Actual vs Predicted')
        plt.legend()
        plt.show()


def train_RNN():
    train_data = pd.read_pickle('train_data.pkl')
    train_data = train_data[feature]

    # 提取特征和目标列
    features = train_data.values  # 前面所有列除了最后5列
    targets = train_data.iloc[:, -5:].values  # 最后5列

    # 标准化特征
    scalerX = joblib_load(rf'standardScalerX.m')
    scalerY = joblib_load(rf'standardScalerY.m')
    x = scalerX.transform(features)
    x = x.reshape(-1, 1, len(feature))
    y = scalerY.transform(targets)

    # 实例化模型和定义损失函数与优化器：
    input_size = len(feature)
    hidden_size = 64
    output_size = 5
    model = RNN_model(input_size, hidden_size, output_size)

    # 将模型移动到GPU上
    device = torch_device('cuda' if cuda.is_available() else 'cpu')
    model = model.to(device)
    criterion = MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    num_epochs = 50
    batch_size = 64

    train_dataset = MyDataset(x, y)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(num_epochs):
        for inputs, labels in train_loader:
            # 将每个batch的输入和标签移到GPU上
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

    # 保存模型
    save({
        'epoch': num_epochs,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss.item(),
    }, 'RNNmodel.pth')


if __name__ == '__main__':
    # predict_BP()
    train_RNN()