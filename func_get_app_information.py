from util import my_APK,save_apk
from datetime import datetime
import pandas as pd
import os
import streamlit as st
def get_file_name(apk_path):
    return apk_path.split('\\')[-1]

def get_scan_time():
    current_time = datetime.now()
    scan_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return scan_time

def get_file_size(apk_path):
    file_size_bytes = os.path.getsize(apk_path)
    file_size = round(file_size_bytes / 1024 / 1024, 1)

    return str(file_size) + 'MB'





def get_app_information(apk_data = None,
                        apk_path : str = 'None' ,
                        progress_callback = None
                        ):

    if apk_path == 'None':
        if apk_data is None:
            print('Invalid input')
            return
        apk_path = save_apk(apk_data)

    st.session_state['static_progress'].append ('初始化分析工具')
    if progress_callback:
        progress_callback()
    tool = my_APK(apk_path)

    methods_dict_1 = {
        'name' : tool.get_app_name,
        'md5' : tool.get_md5,
        'url' : tool.get_url,
        'signature_name' : tool.get_signature_names,
        'package_name' : tool.get_package,
        'version_name' : tool.get_androidversion_name,
        'version_code' : tool.get_androidversion_code,
        'min_sdk' : tool.get_min_sdk_version,
        'max_sdk' : tool.get_max_sdk_version,
        'main_activity' : tool.get_main_activity,
        'activities' : tool.get_activities,
        'services' : tool.get_services,
        'receivers' : tool.get_receivers,
        'providers' : tool.get_providers,
        'details_permissions' : tool.get_permissions_report,
        'permissions' : tool.get_permissions,
        'scan_time' : get_scan_time,
        'icon_path' : tool.get_icon,
    }

    methods_dict_2 ={#args = apk_path
        'file_name' : get_file_name,
        'file_size' : get_file_size,
    }

    data_dict = {
        'two_label':['未识别'],
        'confidence': [1],
        'five_label' : ['未识别'],
        'five_info' : [''],
    }

    for data_name,method in methods_dict_1.items():
        st.session_state['static_progress'].append( '\n提取 '+data_name)
        if progress_callback:
            progress_callback()
        data_dict[data_name] = [method()]

    for data_name,method in methods_dict_2.items():
        st.session_state['static_progress'].append( '\n提取 ' + data_name)
        if progress_callback:
            progress_callback()
        data_dict[data_name] = [method(apk_path)]

    st.session_state['static_progress'].append( '\n提取 ' + 'classes')
    if progress_callback:
        progress_callback()
    data_dict['classes'] = [pd.DataFrame(tool.get_classes())]




    columns = ['file_name', 'name', 'file_size', 'package_name', 'md5',
               'two_label','confidence','five_label', 'signature_name', 'scan_time',
               'details_permissions','version_name', 'version_code', 'min_sdk', 'max_sdk',
               'services','receivers', 'providers', 'permissions',
               'icon_path','url','classes','main_activity','activities']

    df = pd.DataFrame(data_dict)
    df = df[columns]#按columns排序

    return df,apk_path,data_dict['five_info'],tool



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




