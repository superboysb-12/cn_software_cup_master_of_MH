from util import my_APK,save_apk
from datetime import datetime
import pandas as pd
import os
from model_util import Predictor



def get_app_information(apk_data = None,
                        apk_path : str = 'None' ,
                        target_path : str = 'None',
                        rdf : bool = False, #是否要直接返回dataframe而非保存
                        ):

    if apk_path == 'None':
        if apk_data is None:
            print('Invalid input')
            return
        apk_path = save_apk(apk_data)

    tool = my_APK(apk_path)


    file_name = apk_path.split('\\')[-1]
    name = tool.get_app_name()
    current_time = datetime.now()
    scan_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    classes = pd.DataFrame(tool.get_classes())


    md5 = tool.get_md5()
    url = pd.DataFrame(tool.get_url())

    icon = tool.get_icon(target_path=r'temp\icon', target_name=name, image=False)

    file_size_bytes = os.path.getsize(apk_path)
    file_size = round(file_size_bytes/1024/1024,1)
    signature_name = tool.get_signature_names()

    predictor = Predictor()
    predictor.predict(tool.get_info())

    label,confidence =  predictor.predict(tool.get_info())

    package_name = tool.get_package()
    version_name = tool.get_androidversion_name()
    version_code = tool.get_androidversion_code()
    min_sdk = tool.get_min_sdk_version()
    max_sdk = tool.get_max_sdk_version()
    main_activity = tool.get_main_activity()
    activities = tool.get_activities()
    services = tool.get_services()
    receivers = tool.get_receivers()
    providers=tool.get_providers()
    details_permissions=tool.get_permissions_report()
    permissions = tool.get_permissions()


    columns = ['file_name', 'name', 'file_size', 'package_name', 'md5',
               'label','confidence', 'signature_name', 'scan_time','details_permissions',
               'version_name', 'version_code', 'min_sdk', 'max_sdk',
               'services','receivers', 'providers', 'permissions',
               'icon','url','classes','main_activity','activities']

    data = {
        'file_name': [file_name],
        'file_size': [str(file_size)+'MB'],
        'name': [name],
        'package_name': [package_name],
        'md5': [md5],
        'label': [label],
        'confidence': [confidence],
        'signature_name': [signature_name],
        'main_activity': [main_activity],
        'scan_time': [scan_time],
        'version_name': [version_name],
        'version_code': [version_code],
        'min_sdk': [min_sdk],
        'max_sdk': [max_sdk],
        'activities': [activities],
        'services': [services],
        'receivers': [receivers],
        'providers': [providers],
        'permissions': [permissions],
        'icon':[icon],
        'url':[url],
        'classes':[classes],
        'details_permissions':[details_permissions]
    }

    df = pd.DataFrame(data)
    df = df[columns]#按columns排序
    if target_path != 'None':#按分析时间创建csv文件
        if rdf:
            return df
        df.to_csv(target_path + "\\" + ''.join([c for c in scan_time if c != ':' and c != '-' and c != ' ']) + ".csv",
                  encoding='gbk', index=False)
        return target_path + "\\" + ''.join([c for c in scan_time if c != ':' and c != '-' and c != ' ']) + ".csv"

    #返回前端所需数据
    basic = df.loc[:, 'name': 'providers']
    df_transposed = basic.transpose()
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed.drop(df_transposed.index[0])

    #在这里对APK进行解析得到各种特征得到多个df(基本信息, 应用权限, 相关url, 类, activity,image)以及apk_path
    return (df_transposed,details_permissions,url,classes,df.loc[:, ['main_activity','activities']],df['icon']),apk_path




def get_dynamic_analysis_information(file_path):
    data = pd.read_csv(file_path)
    columns = data.columns
    #source ip and counts
    srcs = data[columns[1]].value_counts()
    #destination ip and counts
    dsts = data[columns[2]].value_counts()
    #protocol number, name and counts
    protos = data.loc[:,[columns[4],columns[3]]].value_counts()
    #unique data and counts
    contact = data.loc[:, [columns[1], columns[2],columns[4]]].value_counts()
    datas = [srcs, dsts, protos, contact]
    for i in range(len(datas)):
        datas[i] = pd.DataFrame(datas[i]).reset_index()

    return datas

get_app_information(apk_path=r"D:\学习资料\反炸APP分析\apk\data\体测圈.apk",rdf=True)


