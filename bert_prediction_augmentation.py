import random

from transformers import BertTokenizer, BertForMaskedLM
import logging
import warnings
import string

# 创建不希望被掩码的标点符号和字母列表
exclude_tokens = list(string.ascii_letters) + list(string.punctuation) + ['[CLS]', '[SEP]']

#print(exclude_tokens)



# 忽略日志与警告
logging.getLogger('transformers').setLevel(logging.ERROR)
warnings.filterwarnings('ignore')


# 加载预训练的 BERT 模型和对应的 tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForMaskedLM.from_pretrained('bert-base-chinese')

text = '"Augment" 是英语中的一个动词，意思是"增强"、"扩大"或"增加"。在数据处理和机器学习领域，"数据增强"（data augmentation）指的是通过对原始数据进行一系列变换或操作，生成新的数据样本，从而扩充训练数据集的技术。数据增强在机器学习中起到了至关重要的作用，尤其是在数据量有限的情况下。通过增加数据集中的样本数量和多样性，可以帮助模型更好地泛化到未见过的数据，从而提高模型的性能和鲁棒性。在自然语言处理（NLP）领域，数据增强的技术包括但不限于：'
def augment_text(text :str,mask_prob : float = 0.15,top_k : int = 5):
    l = len(text)
    tokens = [c for c in text]
    random_index = list(set(random.randint(1, l-1) for _ in range(int(l*mask_prob))))
    for index in random_index:
        if tokens[index] in exclude_tokens:
            continue

        tokens[index] = '[MASK]'
        masked_tokens = ''.join(tokens)
        # 使用 tokenizer 对文本进行编码
        inputs = tokenizer(masked_tokens, return_tensors="pt")
        outputs = model(**inputs)

        # 获取预测结果
        predictions = outputs.logits

        # 获取预测结果中 [MASK] 对应的概率分布
        masked_index = inputs["input_ids"].tolist()[0].index(tokenizer.mask_token_id)
        predicted_probabilities = predictions[0, masked_index].softmax(dim=0)

        # 获取预测概率最高的前几个词的索引
        top_indices = predicted_probabilities.topk(top_k).indices.tolist()
        # 使用 tokenizer 将索引转换为对应的词汇
        predicted_tokens = [tokenizer.decode([index]) for index in top_indices]

        #print("预测的词汇：", predicted_tokens)

        tokens[index] = predicted_tokens[random.randint(0,4 )]

    return ''.join(tokens)

print('original: ',text)
print('augmented: ',augment_text(text))


