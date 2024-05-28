import pandas as pd
from gensim.models import KeyedVectors
import jieba
import numpy as np

def load_model():
    try:
        model = KeyedVectors.load_word2vec_format('sgns.merge.word', binary=False)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

model = load_model()

def word_2_vec(text, if_cut_all):
    if model is None:
        return None

    if not isinstance(text, str):
        return None

    seg_list = jieba.cut(text, cut_all=if_cut_all)
    word_vectors = [model[word] for word in seg_list if word in model]
    print("已经完成一次转化！")

    if word_vectors:
        return np.mean(word_vectors, axis=0)
    else:
        return None

df = pd.read_csv('5_26.csv', encoding='GBK')

text_column = 'name'
if_cut_all = False  # 根据需要选择分词模式

df[text_column] = df[text_column].astype(str).fillna('')

df['vector'] = df[text_column].apply(lambda x: word_2_vec(x, if_cut_all))

vector_df = df['vector'].apply(pd.Series)

vector_df.columns = [f'dim_{i}' for i in range(vector_df.shape[1])]

df = pd.concat([df, vector_df], axis=1)

df.drop(columns=['vector'], inplace=True)

df.to_csv('output.csv', index=False, encoding='GBK')
