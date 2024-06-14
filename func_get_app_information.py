from util import my_APK,save_apk
from datetime import datetime
import pandas as pd
import os
from model_util import Predictor



def get_app_information(apk_data = None,
                        apk_path : str = 'None' ,
                        target_path : str = 'None',
                        rdf : bool = False #是否要直接返回dataframe而非保存
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

    classes = tool.get_classes()
    md5 = tool.get_md5()
    url = 'None'#tool.get_url()
    icon = tool.get_icon(target_path=r'temp\icon', target_name=name, image=False)

    file_size_bytes = os.path.getsize(apk_path)
    file_size = round(file_size_bytes/1024/1024,1)
    signature_name = tool.get_signature_names()

    predictor = Predictor()
    predictor.predict(tool.get_info())
    label = '涉诈' if predictor.predict(tool.get_info()) else '非涉诈'

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
               'label', 'signature_name', 'scan_time','details_permissions',
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

    #在这里对APK进行解析得到各种特征得到多个df(基本信息, 应用权限, 相关url, 类, activity)和image 以及apk_path
    return (df_transposed,details_permissions,df['url'],df['classes'],df.loc[:, ['main_activity','activities']],df['icon']),apk_path