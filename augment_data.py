from process_data import strengthen_data
import os
import pandas as pd


'''
#将数据按类型分类
data = pd.read_csv("D:\学习资料\反炸APP分析\Data\\merged.csv",encoding="gbk")
r,c = len(data),len(data.columns)
columns = [data.columns[i] for i in range(c)]

types = data[columns[-1]].unique()

for type in types:
    new_data = data[data[columns[-1]] == type].copy()
    #new_data.drop(columns[-1], axis=1, inplace=True)
    #print(new_data)
    target_path = "D:\学习资料\反炸APP分析\\dataset"
    new_data.to_csv(target_path + '\\' + type + '.csv', index=False, encoding='gbk')
    '''







# 定义文件夹路径
folder_path = 'D:\学习资料\反炸APP分析\\dataset'

# 存储所有 CSV 文件的数据框
all_dataframes = []

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):  # 检查文件扩展名是否为 CSV
        file_path = os.path.join(folder_path, file_name)
        # 读取 CSV 文件并将其添加到列表中
        df = pd.read_csv(file_path,encoding="gbk")
        new_data = strengthen_data(data=df,
                                   target_name=file_name+"(strengthened)",
                                   target_path="D:\学习资料\反炸APP分析\\Data",
                                   target_num= len(df)//2,
                                   merge= True)
        all_dataframes.append(new_data)

ALL = pd.concat(all_dataframes, ignore_index=True)
ALL.to_csv("D:\学习资料\反炸APP分析\\Data"+'\\'+'merged(strengthened)'+'.csv', index=False,encoding='gbk')