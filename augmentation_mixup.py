from func_attribute_mixup import attribute_mixup
import os
import pandas as pd

DATA_PATH = "D:\学习资料\反炸APP分析\Data\output.csv"
CLASS_TARGET_PATH = "D:\学习资料\反炸APP分析\Data" #分类的数据存放地址

TARGET_PATH = "D:\学习资料\反炸APP分析\\augmented_data"#增强数据存放地址
TARGET_NAME = 'merged(augmented)'#(合并的)增强数据文件名

#将数据按类型分类,存放在CLASS_TARGET_PATH
data = pd.read_csv(DATA_PATH,encoding="gbk")
r,c = len(data),len(data.columns)
columns = [data.columns[i] for i in range(c)]
types = data[columns[0]].unique()

for type in types:
    new_data = data[data[columns[0]] == type].copy()
    #new_data.drop(columns[0], axis=1, inplace=True)
    print(new_data)
    target_path = CLASS_TARGET_PATH
    new_data.to_csv(target_path + '\\' + type + '.csv', index=False, encoding='gbk')

#对每个类进行mixup
folder_path = CLASS_TARGET_PATH
all_dataframes = []

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):  # 检查文件扩展名是否为 CSV
        file_path = os.path.join(folder_path, file_name)
        # 读取 CSV 文件并将其添加到列表中
        df = pd.read_csv(file_path, encoding="gbk")
        #mixup
        new_data = attribute_mixup(data=df,
                                   target_name=file_name + "(augmented)",
                                   target_path=TARGET_PATH,
                                   target_num=325,
                                   merge=False)
        all_dataframes.append(new_data)

#保存合并的数据文件
ALL = pd.concat(all_dataframes, ignore_index=True)
ALL.to_csv(TARGET_PATH + '\\' + TARGET_NAME + '.csv', index=False, encoding='gbk')
