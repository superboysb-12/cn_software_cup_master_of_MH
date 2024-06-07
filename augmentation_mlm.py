import random
import pandas as pd
from func_mlm_augmentation import augment_mlm

DATA_PATH = "D:\学习资料\反炸APP分析\Data\output.csv"
TARGET_PATH ="D:\学习资料\反炸APP分析\Data"
TARGET_NAME = "augmented_data_mlm_1"

#读入数据
data = pd.read_csv(DATA_PATH,encoding="gbk")
r = len(data)
columns = data.columns

#存放新数据的变量
new = pd.DataFrame(columns =columns)
new_rows = []

#对文本进行掩码预测
def augmentation_mlm(text : str):# -> str
    #设置一个滑动窗口 大小为size
    size = 256
    n = len(text)
    left,right = -size,0

    new_row = []
    while True:
        left = min(left+size,n)
        right = min(right+size,n)
        if left == n:
            break
        current_text = text[left:right]
        new_text = augment_mlm(current_text,0.2)
        new_row.append(new_text)

    return ' '.join(new_row)

total= 10
for _ in range(total):
    print(_+1,'\\',total)
    index = random.randint(1,r-1)
    label,text = data[columns[0]][index],data[columns[1]][index]
    augmented_text = augmentation_mlm(text)
    print(augmented_text)
    new_row = pd.DataFrame([[label,augmented_text]], columns=columns)
    new_rows.append(new_row)

new = pd.concat([new] + new_rows, ignore_index=True)


new.to_csv(TARGET_PATH+'\\'+TARGET_NAME+'.csv', index=False,encoding='gbk')





