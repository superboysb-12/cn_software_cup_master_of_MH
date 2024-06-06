import pandas as pd
import re

def merge_columns(input_csv, output_csv, remove_words):
    # 读取 CSV 文件，指定编码为 GBK
    df = pd.read_csv(input_csv, encoding='gbk')

    # 检查列数
    if df.shape[1] < 3:
        raise ValueError("CSV 文件至少需要三列")

    # 保留第二列
    second_column = df.iloc[:, 1]

    # 将第三列到最后一列的数据合并在一起，合并后列的数据用逗号分隔
    df['merged'] = df.iloc[:, 2:].astype(str).apply(lambda x: ','.join(x), axis=1)

    # 定义处理函数
    def process_string(s):
        # 替换除英语字符之外的所有字符为空格
        s = re.sub(r'[^a-zA-Z\s]', ' ', s)
        # 替换所有大于两个的空格为一个空格
        s = re.sub(r'\s{2,}', ' ', s)
        # 删除指定列表中的单词
        words = s.split()
        words = [word for word in words if word.lower() not in remove_words]
        return ' '.join(words)

    # 应用处理函数
    df['processed'] = df['merged'].apply(process_string)

    # 将第二列和处理后的合并列进行合并
    df['final'] = second_column.astype(str) + ' ' + df['processed']

    # 创建新的 DataFrame，只保留第一列和最终的合并列
    result_df = pd.DataFrame({
        df.columns[0]: df.iloc[:, 0],
        'final': df['final']
    })

    # 保存到新的 CSV 文件，指定编码为 GBK
    result_df.to_csv(output_csv, index=False, encoding='gbk')

# 示例使用
input_csv = 'input.csv'
output_csv = 'output.csv'
remove_words = ['android', 'launcher', 'permission', 'com','const','interface','content','forace','Activity','Service','Receiver','google','get','CHANGE','USE','']  # 示例删除的单词列表
merge_columns(input_csv, output_csv, remove_words)
