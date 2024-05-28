from gensim.models import KeyedVectors
import jieba

def word_2_vec(text,if_cut_all):
    model = KeyedVectors.load_word2vec_format('sgns.merge.word', binary=False)
    seg_list = jieba.cut(text, cut_all=if_cut_all)

    word_vectors = []

    for word in seg_list:
        try:
            word_vector = model[word]
            word_vectors.append(word_vector)
        except KeyError:
            pass

    if word_vectors:
        sum_vector = sum(word_vectors)
        average_vector = sum_vector / len(word_vectors)
        print("已经完成一次转化！")
        return average_vector
    else:
        return None

