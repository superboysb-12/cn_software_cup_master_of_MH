
from EDA import EDA
import pandas as pd
import random

data = pd.read_csv("D:\学习资料\反炸APP分析\Data\output.csv",encoding="gbk")

r = len(data)
columns = data.columns

def augmentation_EDA(text : str,replace_prob : float = 0.3): # -> str
    eda = EDA()
    words = text.split()
    n = len(words)
    new_words = eda.synonym_replacement(words,max(1,int(n*replace_prob)))
    new_words = eda.random_swap(new_words,max(1,int(n*replace_prob)))
    new_words = eda.random_deletion(new_words)
    new_words = eda.random_insertion(new_words,int(n*0.001))
    return ' '.join(new_words)

new = pd.DataFrame(columns =columns)
new_rows = []
augement_num = 600
for _ in range(augement_num):
    index = random.randint(1,r-1)
    label,text = data[columns[0]][index],data[columns[1]][index]
    augmented_text = augmentation_EDA(text)
    new_row = pd.DataFrame([[label,augmented_text]], columns=columns)
    new_rows.append(new_row)

new = pd.concat([new] + new_rows, ignore_index=True)

target_path = "D:\学习资料\反炸APP分析\Data"
new.to_csv(target_path+'\\'+"augmented_data_EDA"+'.csv', index=False,encoding='gbk')