from EDA import EDA
import pandas as pd
import random

DATA_PATH = "D:\学习资料\反炸APP分析\Data\output.csv"
TARGET_PATH = "D:\学习资料\反炸APP分析\Data"
TARGET_NAME = "augmented_data_EDA"
AUGMENT_NUM = 600 #新增多少数据

#读入数据
data = pd.read_csv(DATA_PATH,encoding="gbk")
r = len(data)
columns = data.columns

#存放新数据的变量
new = pd.DataFrame(columns =columns)
new_rows = []

#对文本使用EDA的四种方法
def augmentation_EDA(text : str,replace_prob : float = 0.3): # -> str
    eda = EDA()
    words = text.split()
    n = len(words)
    new_words = eda.synonym_replacement(words,max(1,int(n*replace_prob)))
    new_words = eda.random_swap(new_words,max(1,int(n*replace_prob)))
    new_words = eda.random_deletion(new_words)
    new_words = eda.random_insertion(new_words,int(n*0.001))
    return ' '.join(new_words)

#600次随机对某一条数据增强,并添加到新数据变量
for _ in range(AUGMENT_NUM):
    index = random.randint(1,r-1)
    label,text = data[columns[0]][index],data[columns[1]][index]
    augmented_text = augmentation_EDA(text)
    new_row = pd.DataFrame([[label,augmented_text]], columns=columns)
    new_rows.append(new_row)

#合并并保存
new = pd.concat([new] + new_rows, ignore_index=True)
new.to_csv(TARGET_PATH+'\\'+TARGET_NAME+'.csv', index=False,encoding='gbk')