import pandas as pd
import random
#同一类型数据的增强
def strengthen_data(file_path : str = 'None',target_path : str = '',target_num : int = 100, data = None):#->dataframe
    #file_path和 data至少一个输入且优先使用file_path
    if file_path !='None':
        data = pd.read_csv(file_path, encoding="gbk")
    else:
        if data == None:
            print('ERROR')
            return
    r,c = len(data),len(data.columns)
    columns = [data.columns[i] for i in range(c)]
    new = pd.DataFrame(columns =columns)
    #数据混合产生新数据
    for _ in range(target_num):
        #产生r个随机数
        random_index = [random.randint(1, r-1) for _ in range(c)]
        #随机组合产生新数据
        new_row = pd.Series([data[columns[i]][random_index[i]] for i in range(c)],index = columns)
        new = new._append(new_row,ignore_index=True)
    new.to_csv(target_path+'\strengthened_data.csv', index=False,encoding='gbk')

    return new

#file_path,target_path = "D:\学习资料\反炸APP分析\Data\data.csv",'D:\学习资料\反炸APP分析\数据增强'
#target_num = 10
#strengthen_data(file_path=file_path,target_path=target_path,target_num=target_num)
