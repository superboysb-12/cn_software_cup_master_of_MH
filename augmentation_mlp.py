import random
import pandas as pd
from func_mlm_augmentation import augment_text
data = pd.read_csv("D:\学习资料\反炸APP分析\Data\output.csv",encoding="gbk")
r = len(data)
columns = data.columns
text = data[columns[1]][0]
#print(len(text),text)
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
        #print(left//size+1,'\\',(n+int(size/2))//size)
        current_text = text[left:right]
        #print('original:\t',current_text)
        new_text = augment_text(current_text,0.2)
        #print('augmented:\t',new_text)
        new_row.append(new_text)


    return ' '.join(new_row)

new = pd.DataFrame(columns =columns)
new_rows = []
total= 10
for _ in range(total):
    print(_+1,'\\',total)
    index = random.randint(1,r-1)
    label,text = data[columns[0]][index],data[columns[1]][index]
    augmented_text = augmentation_mlp(text)
    print(augmented_text)
    new_row = pd.DataFrame([[label,augmented_text]], columns=columns)
    new_rows.append(new_row)

new = pd.concat([new] + new_rows, ignore_index=True)

target_path ="D:\学习资料\反炸APP分析\Data"
new.to_csv(target_path+'\\'+"augmented_data_mlp_1"+'.csv', index=False,encoding='gbk')





