import optuna
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

def train_and_incremental_learning(data_path, model='base_model', new_model='new_model', incremental=True):
    # 读取数据
    data = pd.read_csv(data_path, encoding='ISO-8859-1')

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
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32, callbacks=[early_stop])

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
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=best_params['learning_rate']), metrics=['accuracy'])
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)

    # 保存最佳模型
    model.save(f"models/{new_model}.keras")
    # 在测试集上评估最佳模型
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"最佳模型的准确率是 {accuracy}")
train_and_incremental_learning('../dataset/base.csv',incremental=False)


