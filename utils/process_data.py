from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
from sklearn.manifold import Isomap
import numpy as np
import random

def process_permissions(df):
    df['permissions'] = df['permissions'].apply(eval)

    df['official_permissions'] = df['permissions'].apply(lambda x: [i for i in x if i.startswith('android.permission.')])
    df['customer_permissions'] = df['permissions'].apply(lambda x: [i for i in x if not i.startswith('android.permission.')])

    df['has_customer_permission'] = df['customer_permissions'].apply(lambda x: 0 if len(x) == 0 else 1)

    mlb = MultiLabelBinarizer()
    permissions_binarized = mlb.fit_transform(df['official_permissions'])

    permissions_df = pd.DataFrame(permissions_binarized, columns=mlb.classes_)

    df = pd.concat([df.drop(['permissions', 'official_permissions'], axis=1), permissions_df], axis=1)

    return df

def transform_data(data,target_dimension : int): # -> ndarray
    #数据量与维度
    n_samples,n_features=len(data),len(data[0])
    #创建模型
    isomap = Isomap(n_components=target_dimension)
    # 对数据进行拟合和转换
    transformed_data = isomap.fit_transform(data)
    return transformed_data

def strengthen_data(file_path : str = 'None',
                    target_path : str = '',
                    target_num : int = 100,
                    data = None,target_name : str = "strengthened_data",
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
    #数据混合产生新数据
    for _ in range(target_num):
        #产生r个随机数
        random_index = [random.randint(1, r-1) for _ in range(c)]
        #随机组合产生新数据
        new_row = pd.Series([data[columns[i]][random_index[i]] for i in range(c)],index = columns)
        new = new._append(new_row,ignore_index=True)

    if merge:
        new = pd.concat([new,data], ignore_index=True)
    new.to_csv(target_path+'\\'+target_name+'.csv', index=False,encoding='gbk')

    return new

#df = pd.read_csv('../dataset/merged.csv', encoding='gbk')

#df = process_permissions(df)

#df.to_csv('../dataset/new_merged.csv', index=False,encoding='gbk')