import random

from transformers import BertTokenizer, BertForMaskedLM
import logging
import warnings
import string

# 创建不希望被掩码的标点符号和字母列表
exclude_tokens =  list(string.punctuation) + ['[CLS]', '[SEP]'] #+list(string.ascii_letters)

#print(exclude_tokens)



# 忽略日志与警告
logging.getLogger('transformers').setLevel(logging.ERROR)
warnings.filterwarnings('ignore')


# 加载预训练的 BERT 模型和对应的 tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

#text = 'you should have act, the elder scroll told of their return'
def augment_text(text :str,mask_prob : float = 0.15,top_k : int = 5):

    tokens = text.split()
    l = len(tokens)
    new_tokens = []
    for i in range(l):
        new_tokens.extend([tokens[i],' '])
    tokens = new_tokens
    l = len(tokens)
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

        tokens[index] = predicted_tokens[random.randint(0,top_k-1 )]
    tokens = [word for word in tokens if word != ' ']
    return ' '.join(tokens)

#print('original: ',text)
#print('augmented: ',augment_text(text,mask_prob=0.2))


