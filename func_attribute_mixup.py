import pandas as pd
import random

def attribute_mixup(file_path : str = 'None',#原文件路径
                    target_path : str = '',#目标路径
                    augment_num : int = 10000,#新增多少数据 最终不会超过target_num
                    target_num : int = 325,#增强到多少数据
                    data = None,#原数据
                    target_name : str = "augmented_data",#目标文件名称
                    merge : bool = True#是否要将新增数据与原数据合并
                    ):

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

    #新增数据数量不超过目标数量
    if augment_num+r > target_num:
        augment_num = target_num - r -1

    #数据混合产生新数据
    for _ in range(augment_num):
        random_index = [random.randint(1, r-1) for _ in range(c)]
        new_row = pd.Series([data[columns[i]][random_index[i]] for i in range(c)],index = columns)
        print(new_row)
        new = new._append(new_row,ignore_index=True)

    if merge:
        new = pd.concat([new,data], ignore_index=True)
    new.to_csv(target_path+'\\'+target_name+'.csv', index=False,encoding='gbk')

    return new
