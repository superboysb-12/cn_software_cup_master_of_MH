import optuna
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from tensorflow.keras.models import load_model
from util import APK
import joblib
import os
from sklearn.linear_model import SGDClassifier

def data_process(data):
    # 读取数据
    data = pd.read_csv(data, encoding='ISO-8859-1')

    # 假设 'label' 是我们的目标列
    target_column = 'type'
    X = data.drop(target_column, axis=1)
    y = data[target_column].astype('category').cat.codes.astype('float32')

    # 数据预处理
    #非数值列转换为数值
    for column in X.columns:
        if X[column].dtype == object:
            X[column] = X[column].astype('category').cat.codes
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 将数据重塑为 RNN 所需的形状 (samples, timesteps, features)
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
    return X_train,X_test,y_train,y_test

data_process('../dataset/base.csv')

def train_and_incremental_learning(data_path, model='base_model', new_model='new_model', incremental=True):
    X_train, X_test, y_train, y_test = data_process(data_path)
    # 定义目标函数
    def objective(trial):
        # 定义超参数搜索空间
        rnn_units = trial.suggest_int('rnn_units', 16, 128)  # 扩大 RNN 单元的搜索范围
        dropout_rate = trial.suggest_float('dropout_rate', 0.0, 0.8)  # 扩大 dropout 率的搜索范围
        learning_rate = trial.suggest_loguniform('learning_rate', 1e-6, 1e-1)  # 扩大学习率的搜索范围
        activation = trial.suggest_categorical('activation', ['relu', 'tanh', 'sigmoid'])  # 添加激活函数作为超参数

        # 初始化模型
        model = Sequential()
        model.add(SimpleRNN(rnn_units, input_shape=(X_train.shape[1], X_train.shape[2])))
        model.add(Dropout(dropout_rate))
        model.add(Dense(1, activation=activation))  # 使用搜索到的激活函数
        model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=learning_rate), metrics=['accuracy'])

        # 训练模型
        early_stop = EarlyStopping(monitor='val_loss', patience=3)
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=32, callbacks=[early_stop])

        # 在验证集上评估模型
        loss, accuracy = model.evaluate(X_test, y_test)
        return accuracy

    # 创建一个新的 Optuna study
    study = optuna.create_study(direction='maximize')

    # 优化目标函数
    study.optimize(objective, n_trials=100)

    # 输出最佳的超参数
    print("Best trial:")
    trial = study.best_trial
    print("  Value: ", trial.value)
    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))

    # 使用最佳的超参数重新训练模型
    best_params = study.best_params
    model = Sequential()
    model.add(SimpleRNN(best_params['rnn_units'], input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(best_params['dropout_rate']))
    model.add(Dense(1, activation=tanh))
    model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=best_params['learning_rate']), metrics=['accuracy'])
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=64)

    # 保存最佳模型
    model.save(f"models/{new_model}.keras")
    # 在测试集上评估最佳模型
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"最佳模型的准确率是 {accuracy}")
#train_and_incremental_learning('../dataset/base2.csv',incremental=False)

def check_non_empty(*args):
    for string in args:
        if string:
            return True
    return False

def predict_with_model(model, apk_path):
    data = []
    try:
        apk = APK(apk_path)
        name = apk.get_app_name()
        permissions = apk.get_permissions()
        packagename = apk.get_package()
        version = apk.get_androidversion_code()
        signature = apk.get_signature_names()

        if check_non_empty(name, permissions, packagename, version, signature):
            data = pd.DataFrame([name] + permissions + [packagename, version, signature])
    except Exception as e:
        print(f"处理APK文件时出错: {apk_path}, 错误: {str(e)}")
        return

    for column in data.columns:
        if data[column].dtype == object:
            data[column] = data[column].astype('category').cat.codes

    # 使用 StandardScaler 进行归一化
    scaler = StandardScaler()
    data = scaler.fit_transform(data)

    # 将数据重塑为 RNN 所需的形状 (samples, timesteps, features)
    data = np.reshape(data, (15, 1, 5))

    # 加载模型
    model = load_model(f"models/{model}.keras")

    # 使用模型进行预测
    prediction = model.predict(data)

    # 打印预测结果
    print(f"预测结果为: {prediction}")


#predict_with_model('new_model', 'apks/lm.apk')


def train_and_incremental_learning(data_path, model='base_model', new_model='new_model', incremental=True):
    # 读取数据
    data = pd.read_csv(data_path, encoding='gbk')

    # 假设 'label' 是我们的目标列
    target_column = 'type'
    X = data.drop(target_column, axis=1)
    y = data[target_column]

    # 数据预处理
    #非数值列转换为数值
    for column in X.columns:
        if X[column].dtype == object:
            X[column] = X[column].astype('category').cat.codes

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 检查模型是否存在
    if os.path.exists(f"models/{model}") and incremental:
        # 加载模型
        clf = joblib.load(f"models/{model}")
        # 检查模型是否有 'partial_fit' 方法
        if not hasattr(clf, 'partial_fit'):
            print("该模型不支持增量学习。")
            return clf
        clf.partial_fit(X_train, y_train, classes=np.unique(y))
        joblib.dump(clf, f"models/{new_model}")
    else:
        # 初始化模型
        clf = SGDClassifier()
        clf.fit(X_train, y_train)
        joblib.dump(clf,f"models/{model}")

    # 在测试集上评估模型
    accuracy = clf.score(X_test, y_test)
    print(f"模型的准确率是 {accuracy}")

train_and_incremental_learning('../dataset/base2.csv',incremental=False)