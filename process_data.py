import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

def process_permissions(df):
    df['permissions'] = df['permissions'].apply(eval)

    mlb = MultiLabelBinarizer()
    permissions_binarized = mlb.fit_transform(df['permissions'])

    permissions_df = pd.DataFrame(permissions_binarized, columns=mlb.classes_)

    df = pd.concat([df.drop('permissions', axis=1), permissions_df], axis=1)

    return df

df = pd.read_csv('../dataset/merged.csv', encoding='gbk')

df = process_permissions(df)

df.to_csv('../dataset/new_merged.csv', index=False,)