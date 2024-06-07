from util import my_APK
from func_get_icon import get_icon
from datetime import datetime
import pandas as pd
import os
from androguard.core.bytecodes.apk import APK

CONST_SAVE_PATH = r"temp\apk"



def save_apk(apk_data): # -> str save_path
    current_time = datetime.now()
    time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    save_path = CONST_SAVE_PATH +'\\'+''.join([c for c in time if c != ':' and c != '-' and c != ' ' ])+r".apk"
    with open(save_path, "wb") as f:
        f.write(apk_data)

    return save_path




def get_app_information(apk_data = None, apk_path : str = 'None' , target_path : str = 'None'):# -> information_path #csv和png均保存在target_path
    if apk_path == 'None':
        if apk_data is None:
            print('Invalid input')
            return
        apk_path = save_apk(apk_data)



    tool = my_APK(apk_path)
    too = APK(apk_path)

    file_name = apk_path.split('\\')[-1]


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

    url = 'None'#tool.get_url()
    classes = tool.get_classes()

    icon = get_icon(apk_path = apk_path,target_path=target_path,target_name=name,image=False) if target_path != 'None' \
        else get_icon(apk_path = apk_path,target_path=CONST_SAVE_PATH,target_name=name,image=False)

    columns = ['file_name', 'name', 'file_size', 'package_name', 'md5',
               'label', 'signature_name', 'scan_time',
               'version_name', 'version_code', 'min_sdk', 'max_sdk',
               'services','receivers', 'providers', 'permissions',
               'andro_permissions','icon','url','classes','main_activity','activities']

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
        'andro_permissions': [andro_permissions],
        'icon':[icon],
        'url':[url],
        'classes':[classes]
    }

    df = pd.DataFrame(data)
    df = df[columns]#按columns排序
    basic = df.loc[:, 'name': 'providers']

    #在这里对APK进行解析得到各种特征得到多个df(基本信息, 应用权限, 相关url, 类, activity)和image
    if target_path == 'None':
        return basic,df['permissions'],df['url'],df['classes'],df.loc[:, ['main_activity','activities']],df['icon']
    df.to_csv(target_path+"\\"+''.join([c for c in scan_time if c != ':' and c != '-' and c != ' ' ])+".csv",encoding='gbk',index=False)

    return target_path+"\\"+''.join([c for c in scan_time if c != ':' and c != '-' and c != ' ' ])+".csv"
#get_app_information(r"D:\学习资料\反炸APP分析\apk\data\体测圈.apk.1",r"D:\学习资料\反炸APP分析\apk\data")