
import pandas as pd
data = pd.read_csv("D:\学习资料\反炸APP分析\Data\output.csv",encoding="gbk")
r = len(data)
columns = data.columns
text = data[columns[1]][0]
#print(len(text),text)
from func_mlm_augmentation import augment_text
def augmentation_mlp(text : str):# -> str
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
        print(left//size+1,'\\',(n+int(size/2))//size)
        current_text = text[left:right]
        #print('original:\t',current_text)
        new_text = augment_text(current_text,0.2)
        #print('augmented:\t',new_text)
        new_row.append(new_text)


    return ' '.join(new_row)

print(augmentation_mlp(text))





