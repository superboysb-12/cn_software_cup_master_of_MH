import pandas as pd
import random

#同一类型数据的增强

def strengthen_data(file_path : str = 'None',
                    target_path : str = '',
                    augment_num : int = 10000,#新增多少数据 最终不会超过target_num
                    target_num : int = 325,#增强到多少数据
                    data = None,target_name : str = "augmented_data",
                    merge : bool = True):

    #file_path和 data至少一个输入且优先使用file_path
    if file_path !='None':
        data = pd.read_csv(file_path, encoding="gbk")
    else:
        if data is None:
            print('ERROR')
            return
    r,c = len(data),len(data.columns)
    columns = [data.columns[i] for i in range(c)]
    new = pd.DataFrame(columns =columns)
    if augment_num+r > target_num:
        augment_num = target_num - r -1
    #数据混合产生新数据
    for _ in range(augment_num):
        #产生c个随机数
        random_index = [random.randint(1, r-1) for _ in range(c)]
        #随机组合产生新数据
        new_row = pd.Series([data[columns[i]][random_index[i]] for i in range(c) ],index = columns)
        print(new_row)
        new = new._append(new_row,ignore_index=True)

    if merge:
        new = pd.concat([new,data], ignore_index=True)
    new.to_csv(target_path+'\\'+target_name+'.csv', index=False,encoding='gbk')

    return new

'''
file_path,target_path = "D:\学习资料\反炸APP分析\dataset\\white.csv",'D:\学习资料\反炸APP分析\Data'
target_num = 325
data = pd.read_csv(file_path, encoding="gbk")
strengthen_data(data=data,target_path=target_path,target_num=target_num)
'''