from sklearn.manifold import Isomap
import numpy as np
#data = list(np.random.randint(0, 2, size=(100, 200)))
def transform_data(data,target_dimension : int): # -> ndarray
    #数据量与维度
    n_samples,n_features=len(data),len(data[0])
    #创建模型
    isomap = Isomap(n_components=target_dimension)
    # 对数据进行拟合和转换
    transformed_data = isomap.fit_transform(data)
    return transformed_data

#print(transform_data(data,5))
