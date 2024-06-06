from util import my_APK
from func_get_icon import get_icon
from datetime import datetime
import pandas as pd
import os
from androguard.core.bytecodes.apk import APK



def get_app_information(apk_path,target_path : str  = 'None'):# ->information or information_path #csv和png均保存在target_path
    tool = my_APK(apk_path)
    too = APK(apk_path)

    if type(apk_path) == str:
        file_name = apk_path.split('\\')[-1]
    else:
        file_name = too.get_app_name()

    file_size_bytes = os.path.getsize(apk_path)
    file_size = round(file_size_bytes/1024/1024,1)

    name = tool.get_app_name()

    signature_name = tool.get_signature_names()[0]

    #label = tool.get_score()
    label = "?"

    md5 = tool.get_md5()[0]

    package_name = tool.get_package()

    current_time = datetime.now()
    scan_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    version_name = too.get_androidversion_name()
    version_code = too.get_androidversion_code()

    min_sdk = too.get_min_sdk_version()
    max_sdk = too.get_max_sdk_version()

    main_activity = tool.get_main_activity()
    activities = too.get_activities()
    services = tool.get_services()


    receivers = too.get_receivers()
    providers=too.get_providers()

    andro_permissions=too.get_details_permissions()
    permissions = tool.get_permissions()

    get_icon(apk_path,target_path,name)
    icon_path = target_path+'\\'+name+'.png'

    columns = ['file_name', 'file_size', 'name', 'package_name', 'md5', 'label', 'signature_name', 'main_activity',
               'scan_time', 'version_name', 'version_code', 'min_sdk', 'max_sdk', 'activities', 'services',
                'receivers', 'providers', 'permissions','andro_permissions','icon_path']

    data = {
        'file_name': [file_name],
        'file_size': [file_size],
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
        'andro_permissions': [andro_permissions],
        'icon_path':[icon_path]
    }

    df = pd.DataFrame(data)
    df = df[columns]#按columns排序
    if target_path == 'None':
        return df
    df.to_csv(target_path+"\\"+''.join([c for c in scan_time if c != ':' and c != '-' and c != ' ' ])+".csv",encoding='gbk',index=False)
    return target_path+"\\"+''.join([c for c in scan_time if c != ':' and c != '-' and c != ' ' ])+".csv"
#get_app_information(r"D:\学习资料\反炸APP分析\apk\data\体测圈.apk.1",r"D:\学习资料\反炸APP分析\apk\data")