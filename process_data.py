from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd

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

df = pd.read_csv('../dataset/merged.csv', encoding='gbk')

df = process_permissions(df)

df.to_csv('../dataset/new_merged.csv', index=False,encoding='gbk')