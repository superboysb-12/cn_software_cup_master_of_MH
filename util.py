import hashlib
import re
from androguard.misc import AnalyzeAPK
import zipfile
from datetime import datetime
import pandas as pd
import base64
from transformers import BertTokenizer, BertModel
import tldextract
import sqlite3
import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
from pyzbar.pyzbar import decode
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np
import streamlit as st
from urllib.parse import urljoin
import socket
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def check_all_directories_and_create():
    directories = [
        ['temp'],
        ['temp','apk'],
        ['temp','data'],
        ['temp','icon'],
        ['temp','PDF'],
        ['temp','capture']
    ]
    for directory in directories:
        path = os.path.join(*directory)
        create_directory_if_not_exists(path)

#set_log("ERROR")  # set log message only ERROR

APK_SAVE_PATH = os.path.join('temp','apk')

CHECKPOINT_FILE = os.path.join('model','max.pt')
labels = {'white': 0, 'sex': 1, 'scam': 2, 'gamble': 3, 'black': 4}
id_to_label = {v: k for k, v in labels.items()}

pm = ['android.permission.ACCEPT_HANDOVER', 'android.permission.ACCESS_ADSERVICES_AD_ID',
      'android.permission.ACCESS_ADSERVICES_ATTRIBUTION', 'android.permission.ACCESS_ALL_DOWNLOADS',
      'android.permission.ACCESS_ALL_EXTERNAL_STORAGE', 'android.permission.ACCESS_ASSISTED_GPS',
      'android.permission.ACCESS_BACKGROUND_LOCATION', 'android.permission.ACCESS_BLUETOOTH_SHARE',
      'android.permission.ACCESS_CACHE_FILESYSTEM', 'android.permission.ACCESS_CHECKIN_PROPERTIES',
      'android.permission.ACCESS_COARSE_LOCATION', 'android.permission.ACCESS_COARSE_UPDATES',
      'android.permission.ACCESS_COARSEs_LOCATION_LOCATION', 'android.permission.ACCESS_DOWNLOAD_MANAGER',
      'android.permission.ACCESS_DOWNLOAD_MANAGER_ADVANCED', 'android.permission.ACCESS_FINE_LOCATION',
      'android.permission.ACCESS_GPS', 'android.permission.ACCESS_INSTANT_APPS', 'android.permission.ACCESS_LOCATION',
      'android.permission.ACCESS_LOCATION_EXTRA_COMMANDS', 'android.permission.ACCESS_MEDIA_LOCATION',
      'android.permission.ACCESS_MEMORY', 'android.permission.ACCESS_MOCK_LOCATION',
      'android.permission.ACCESS_NETWORK_CONDITIONS', 'android.permission.ACCESS_NETWORK_STATE',
      'android.permission.ACCESS_NOTIFICATIONS', 'android.permission.ACCESS_NOTIFICATION_POLICY',
      'android.permission.ACCESS_SUPERUSER', 'android.permission.ACCESS_SURFACE_FLINGER',
      'android.permission.ACCESS_WIFI_STATE', 'android.permission.ACCESS_WIMAX_STATE',
      'android.permission.ACCES_MOCK_LOCATION', 'android.permission.ACCGoodsManageActivityESS_WIFI_STATE',
      'android.permission.ACCOUNT_MANAGER', 'android.permission.ACTION_SCREEN_OOF',
      'android.permission.ACTION_USER_PRESENT', 'android.permission.ACTIVITY_EMBEDDING',
      'android.permission.ACTIVITY_RECOGNITION', 'android.permission.ADD_VOICEMAIL', 'android.permission.ALARM_LOCK',
      'android.permission.ALLOCATE_AGGRESSIVE', 'android.permission.ANSWER_PHONE_CALLS',
      'android.permission.AUDIO_CAPTURE', 'android.permission.AUTHENTICATE_ACCOUNTS', 'android.permission.BACKUP',
      'android.permission.BAIDU_LOCATION_SERVICE', 'android.permission.BATTERY_STATS',
      'android.permission.BIND_ACCESSIBILITY_SERVICE', 'android.permission.BIND_APPWIDGET',
      'android.permission.BIND_DEVICE_ADMIN', 'android.permission.BIND_DIRECTORY_SEARCH',
      'android.permission.BIND_NOTIFICATION_LISTENER_SERVICE', 'android.permission.BIND_VPN_SERVICE',
      'android.permission.BLUETOOTH', 'android.permission.BLUETOOTH_ADMIN', 'android.permission.BLUETOOTH_ADVERTISE',
      'android.permission.BLUETOOTH_CONNECT', 'android.permission.BLUETOOTH_PRIVILEGED',
      'android.permission.BLUETOOTH_SCAN', 'android.permission.BODY_SENSORS',
      'android.permission.BROADCAST_PACKAGE_ADDED', 'android.permission.BROADCAST_PACKAGE_CHANGED',
      'android.permission.BROADCAST_PACKAGE_INSTALL', 'android.permission.BROADCAST_PACKAGE_REPLACED',
      'android.permission.BROADCAST_SMS', 'android.permission.BROADCAST_STICKY',
      'android.permission.BROADCAST_WAP_PUSH', 'android.permission.CALL_PHONE', 'android.permission.CALL_PRIVILEGED',
      'android.permission.CAMERA', 'android.permission.CAMERA2', 'android.permission.CAPTURE_AUDIO_HOTWORD',
      'android.permission.CAPTURE_AUDIO_OUTPUT', 'android.permission.CAPTURE_SECURE_VIDEO_OUTPUT',
      'android.permission.CAPTURE_VIDEO_OUTPUT', 'android.permission.CHANGE_APP_IDLE_STATE',
      'android.permission.CHANGE_COMPONENT_ENABLED_STATE', 'android.permission.CHANGE_CONFIGURATION',
      'android.permission.CHANGE_DEVICE_IDLE_TEMP_WHITELIST', 'android.permission.CHANGE_NETWORK_SATET',
      'android.permission.CHANGE_NETWORK_STATE', 'android.permission.CHANGE_OVERLAY_PACKAGES',
      'android.permission.CHANGE_WIFI_MULTICAST_STATE', 'android.permission.CHANGE_WIFI_STATE',
      'android.permission.CHANGE_WIMAX_STATE', 'android.permission.CLEAR_APP_CACHE',
      'android.permission.CLEAR_APP_USER_DATA', 'android.permission.CLEAR_CACHE',
      'android.permission.CONFIGURE_DISPLAY_COLOR_MODE', 'android.permission.CONFIGURE_WIFI_DISPLAY',
      'android.permission.CONNECTIVITY_INTERNAL', 'android.permission.CONNECTIVITY_USE_RESTRICTED_NETWORKS',
      'android.permission.CONTROL_DISPLAY_SATURATION', 'android.permission.CONTROL_INCALL_EXPERIENCE',
      'android.permission.CONTROL_KEYGUARD_SECURE_NOTIFICATIONS', 'android.permission.CONTROL_LOCATION_UPDATES',
      'android.permission.COPY_PROTECTED_DATA', 'android.permission.DELETE_CACHE_FILES',
      'android.permission.DELETE_PACKAGES', 'android.permission.DETECT_SCREEN_CAPTURE',
      'android.permission.DEVICE_POWER', 'android.permission.DIAGNOSTIC', 'android.permission.DISABLE_KEYGUARD',
      'android.permission.DISABLE_STATUS_BAR', 'android.permission.DISPATCH_PROVISIONING_MESSAGE',
      'android.permission.DOWNLOAD_WITHOUT_NOTIFICATION', 'android.permission.DUMP',
      'android.permission.EXPAND_STATUS_BAR', 'android.permission.FLASHLIGHT', 'android.permission.FORCE_BACK',
      'android.permission.FORCE_STOP_PACKAGES', 'android.permission.FOREGROUND_SERVICE',
      'android.permission.FOREGROUND_SERVICER', 'android.permission.FOREGROUND_SERVICE_CAMERA',
      'android.permission.FOREGROUND_SERVICE_MICROPHONE', 'android.permission.FOREGROUND_SERVICE_SPECIAL_USE',
      'android.permission.GET_ACCOUNTS', 'android.permission.GET_ACCOUNTS_PRIVILEGED',
      'android.permission.GET_APP_OPS_STATS', 'android.permission.GET_CLIPS', 'android.permission.GET_DETAILED_TASKS',
      'android.permission.GET_INSTALLED_APPS', 'android.permission.GET_INTENT_SENDER_INTENT',
      'android.permission.GET_PACKAGE_SIZE', 'android.permission.GET_TASKS', 'android.permission.GET_TOP_ACTIVITY_INFO',
      'android.permission.GRANT_RUNTIME_PERMISSIONS', 'android.permission.HARDWARE_TEST',
      'android.permission.HIDE_NON_SYSTEM_OVERLAY_WINDOWS', 'android.permission.HIDE_OVERLAY_WINDOWS',
      'android.permission.HIGH_SAMPLING_RATE_SENSORS', 'android.permission.INSTALL_GRANT_RUNTIME_PERMISSIONS',
      'android.permission.INSTALL_LOCATION_PROVIDER', 'android.permission.INSTALL_PACKAGES',
      'android.permission.INSTALL_PACKAGES_SKY', 'android.permission.INSTALL_SHORTCUT',
      'android.permission.INSTANT_APP_FOREGROUND_SERVICE', 'android.permission.INTENT_FILTER_VERIFICATION_AGENT',
      'android.permission.INTERACT_ACROSS_PROFILES', 'android.permission.INTERACT_ACROSS_USERS',
      'android.permission.INTERACT_ACROSS_USERS_FULL', 'android.permission.INTERNAL_SYSTEM_WINDOW',
      'android.permission.INTERNET', 'android.permission.INVOKE_CARRIER_SETUP', 'android.permission.JPUSH_MESSAGE',
      'android.permission.KILL_BACKGROUND_PROCESSES', 'android.permission.LAUNCH_TWO_PANE_SETTINGS_DEEP_LINK',
      'android.permission.LOADER_USAGE_STATS', 'android.permission.LOCAL_MAC_ADDRESS',
      'android.permission.LOCATION_HARDWARE', 'android.permission.LOCK_DEVICE', 'android.permission.MANAGE_ACCOUNT',
      'android.permission.MANAGE_ACCOUNTS', 'android.permission.MANAGE_ACTIVITY_STACKS',
      'android.permission.MANAGE_APP_OPS_MODES', 'android.permission.MANAGE_APP_OPS_RESTRICTIONS',
      'android.permission.MANAGE_DEVICE_ADMINS', 'android.permission.MANAGE_DOCUMENTS',
      'android.permission.MANAGE_EXTERNAL_STORAGE', 'android.permission.MANAGE_FACTORY_RESET_PROTECTION',
      'android.permission.MANAGE_FINGERPRINT', 'android.permission.MANAGE_MEDIA_PROJECTION',
      'android.permission.MANAGE_NEWLAND', 'android.permission.MANAGE_NEWLANDUART3',
      'android.permission.MANAGE_NOTIFICATIONS', 'android.permission.MANAGE_OWN_CALLS',
      'android.permission.MANAGE_PROFILE_AND_DEVICE_OWNERS', 'android.permission.MANAGE_ROLLBACKS',
      'android.permission.MANAGE_SOUND_TRIGGER', 'android.permission.MANAGE_SUBSCRIPTION_PLANS',
      'android.permission.MANAGE_USB', 'android.permission.MANAGE_USERS',
      'android.permission.MANAGE_USER_OEM_UNLOCK_STATE', 'android.permission.MANAGE_VOICE_KEYPHRASES',
      'android.permission.MASTER_CLEAR', 'android.permission.MODIFY_AUDIO_ROUTING',
      'android.permission.MODIFY_AUDIO_SETTINGS', 'android.permission.MODIFY_DAY_NIGHT_MODE',
      'android.permission.MODIFY_NETWORK_ACCOUNTING', 'android.permission.MODIFY_PHONE_STATE',
      'android.permission.MOUNT_FORMAT_FILESYSTEMS', 'android.permission.MOUNT_UNMOUNT_FILESYSTEMS',
      'android.permission.MOVE_PACKAGE', 'android.permission.NEARBY_WIFI_DEVICES', 'android.permission.NETWORK',
      'android.permission.NETWORK_PROVIDER', 'android.permission.NETWORK_SETTINGS',
      'android.permission.NEW_OUTGOING_CALL', 'android.permission.NFC', 'android.permission.NOTIFICATION_SERVICE',
      'android.permission.NOTIFY_PENDING_SYSTEM_UPDATE', 'android.permission.OBSERVE_GRANT_REVOKE_PERMISSIONS',
      'android.permission.OEM_UNLOCK_STATE', 'android.permission.OVERRIDE_COMPAT_CHANGE_CONFIG_ON_RELEASE_BUILD',
      'android.permission.OVERRIDE_WIFI_CONFIG', 'android.permission.PACKAGE_ADDED',
      'android.permission.PACKAGE_USAGE_STATS', 'android.permission.PACKAGE_VERIFICATION_AGENT',
      'android.permission.PEERS_MAC_ADDRESS', 'android.permission.PERMISSIONS_STORAGE',
      'android.permission.PERSISTENT_ACTIVITY', 'android.permission.POST_NOTIFICATIONS',
      'android.permission.PREVENT_POWER_KEY', 'android.permission.PRE_FACTORY_RESET',
      'android.permission.PROCESS_CPU_USAGE', 'android.permission.PROCESS_OUTGOING_CALLS',
      'android.permission.PROVIDE_RESOLVER_RANKER_SERVICE', 'android.permission.PROVIDE_TRUST_AGENT',
      'android.permission.QUERY_ALL_PACKAGES', 'android.permission.R', 'android.permission.RAISED_THREAD_PRIORITY',
      'android.permission.READCON', 'android.permission.READ_APN_SETTINGS', 'android.permission.READ_APP_BADGE',
      'android.permission.READ_CALENDAR', 'android.permission.READ_CALL_LOG', 'android.permission.READ_CELL_BROADCASTS',
      'android.permission.READ_CLIPBOARD', 'android.permission.READ_CLIPS', 'android.permission.READ_CONTACTS',
      'android.permission.READ_DEVICE_CONFIG', 'android.permission.READ_DREAM_STATE',
      'android.permission.READ_EXTERNAL_STORAGE', 'android.permission.READ_INSTALL_SESSIONS',
      'android.permission.READ_INTERNAL_STORAGE', 'android.permission.READ_LOGS', 'android.permission.READ_MEDIA_AUDIO',
      'android.permission.READ_MEDIA_IMAGES', 'android.permission.READ_MEDIA_STORAGE',
      'android.permission.READ_MEDIA_VIDEO', 'android.permission.READ_MEDIA_VISUAL_USER_SELECTED',
      'android.permission.READ_NETWORK_USAGE_HISTORY', 'android.permission.READ_OEM_UNLOCK_STATE',
      'android.permission.READ_OWNER_DATA', 'android.permission.READ_PACKAGE_BADGE',
      'android.permission.READ_PHONE_NUMBERS', 'android.permission.READ_PHONE_SINTERNETWIFI_STATE',
      'android.permission.READ_PHONE_STATE', 'android.permission.READ_PRECISE_PHONE_STATE',
      'android.permission.READ_PRINT_SERVICES', 'android.permission.READ_PRIVILEGED_PHONE_STATE',
      'android.permission.READ_PROFILE', 'android.permission.READ_RUNTIME_PROFILES',
      'android.permission.READ_SEARCH_INDEXABLES', 'android.permission.READ_SETTINGS', 'android.permission.READ_SMS',
      'android.permission.READ_SOCIAL_STREAM', 'android.permission.READ_SYNC_SETTINGS',
      'android.permission.READ_SYNC_STATS', 'android.permission.READ_USER_DICTIONARY',
      'android.permission.READ_WIFI_CREDENTIAL', 'android.permission.REAL_GET_TASKS', 'android.permission.REBOOT',
      'android.permission.RECEIVE_BOOT_COMPLETED', 'android.permission.RECEIVE_DATA_ACTIVITY_CHANGE',
      'android.permission.RECEIVE_MMS', 'android.permission.RECEIVE_SMS', 'android.permission.RECEIVE_USER_PRESENT',
      'android.permission.RECEIVE_WAP_PUSH', 'android.permission.RECORD_AUDIO', 'android.permission.RECORD_VIDEO',
      'android.permission.RECOVERY', 'android.permission.RECOVER_KEYSTORE', 'android.permission.REGISTER_CALL_PROVIDER',
      'android.permission.REMOTE_AUDIO_PLAYBACK', 'android.permission.REMOTE_DISPLAY_PROVIDER',
      'android.permission.REORDER_TASKS', 'android.permission.REPLACE_EXISTING_PACKAGE',
      'android.permission.REQUEST_COMPANION_RUN_IN_BACKGROUND',
      'android.permission.REQUEST_COMPANION_USE_DATA_IN_BACKGROUND', 'android.permission.REQUEST_DELETE_PACKAGES',
      'android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS', 'android.permission.REQUEST_INSTALL_PACKAGES',
      'android.permission.REQUEST_NETWORK_SCORES', 'android.permission.RESET_PASSWORD',
      'android.permission.RESTART_PACKAGE', 'android.permission.RESTART_PACKAGES',
      'android.permission.REVOKE_RUNTIME_PERMISSIONS', 'android.permission.REZAD_LOGS',
      'android.permission.RUN_INSTRUMENTATION', 'android.permission.SCHEDULE_EXACT_ALARM',
      'android.permission.SCORE_NETWORKS', 'android.permission.SENDTO',
      'android.permission.SEND_DEVICE_CUSTOMIZATION_READY', 'android.permission.SEND_DOWNLOAD_COMPLETED_INTENTS',
      'android.permission.SEND_RESPOND_VIA_MESSAGE', 'android.permission.SEND_SMS',
      'android.permission.SEND_SMS_NO_CONFIRMATION', 'android.permission.SENSOR_ENABLE',
      'android.permission.SENSOR_INFO', 'android.permission.SET_DEBUG_APP',
      'android.permission.SET_HARMFUL_APP_WARNINGS', 'android.permission.SET_KEYBOARD_LAYOUT',
      'android.permission.SET_ORIENTATION', 'android.permission.SET_POINTER_SPEED',
      'android.permission.SET_PREFERRED_APPLICATIONS', 'android.permission.SET_TIME',
      'android.permission.SET_TIME_ZONE', 'android.permission.SET_WALLPAPER', 'android.permission.SET_WALLPAPER_HINTS',
      'android.permission.SHUTDOWN', 'android.permission.SIM_STATE_READY', 'android.permission.SMARTCARD',
      'android.permission.START_ACTIVITIES_FROM_BACKGROUND', 'android.permission.START_ANY_ACTIVITY',
      'android.permission.START_TASKS_FROM_RECENTS', 'android.permission.START_VIEW_PERMISSION_USAGE',
      'android.permission.STATUS_BAR', 'android.permission.SUBSCRIBED_FEEDS_READ',
      'android.permission.SUBSCRIBED_FEEDS_WRITE', 'android.permission.SUBSTITUTE_NOTIFICATION_APP_NAME',
      'android.permission.SUBSTITUTE_SHARE_TARGET_APP_NAME_AND_ICON', 'android.permission.SYSTEM_ALERT_WINDOW',
      'android.permission.SYSTEM_OVERLAY_WINDOW', 'android.permission.TETHER_PRIVILEGED',
      'android.permission.TRANSMIT_IR', 'android.permission.UNINSTALL_SHORTCUT', 'android.permission.UPDATE_APP_BADGE',
      'android.permission.UPDATE_APP_OPS_STATS', 'android.permission.UPDATE_DEVICE_STATS',
      'android.permission.USER_ACTIVITY', 'android.permission.USE_BIOMETRIC', 'android.permission.USE_CREDENTIALS',
      'android.permission.USE_EXACT_ALARM', 'android.permission.USE_FACERECOGNITION',
      'android.permission.USE_FINGERPRIN', 'android.permission.USE_FINGERPRINT',
      'android.permission.USE_FULL_SCREEN_INTENT', 'android.permission.USE_SIP', 'android.permission.UWB',
      'android.permission.VIBRATE', 'android.permission.VIDEO_CAPTURE', 'android.permission.WAKE LOCK',
      'android.permission.WAKELOCK', 'android.permission.WAKE_LOCK', 'android.permission.WRITE_APN_SETTINGS',
      'android.permission.WRITE_APP_BADGE', 'android.permission.WRITE_CALENDAR', 'android.permission.WRITE_CALL_LOG',
      'android.permission.WRITE_CLIPS', 'android.permission.WRITE_CONTACTS', 'android.permission.WRITE_DEVICE_CONFIG',
      'android.permission.WRITE_DREAM_STATE', 'android.permission.WRITE_EXTERNAL_STORAGE',
      'android.permission.WRITE_GSERVICES', 'android.permission.WRITE_INTERNAL_STORAGE',
      'android.permission.WRITE_MEDIA_STORAGE', 'android.permission.WRITE_OWNER_DATA',
      'android.permission.WRITE_PROFILE', 'android.permission.WRITE_SDCARD', 'android.permission.WRITE_SECURE_SETTINGS',
      'android.permission.WRITE_SETTINGS', 'android.permission.WRITE_SMS', 'android.permission.WRITE_SOCIAL_STREAM',
      'android.permission.WRITE_SYNC_SETTINGS', 'android.permission.WRITE_USER_DICTIONARY',
      'android.permission.WRITE_VOICEMAIL', 'android.permission.ZTE_HEARTYSERVICE_MANAGEMENT',
      'android.permission.com.ab.p6768.permission.JPUSH_MESSAGE', 'android.permission.qqmusic.qqcbdm',
      'android.permission.sec.ENTERPRISE_DEVICE_ADMIN', 'android.permission.sec.MDM_CERTIFICATE',
      'android.permission.sec.MDM_SECURITY', 'android.permission.status_bar', 'android.permission.MICROPHONE']

remove_words = ['android', 'launcher', 'permission', 'com', 'const', 'interface', 'content', 'forace', 'Activity',
                'Service', 'Receiver', 'google', 'get', 'CHANGE', 'USE']


def get_ip(url):
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except:
        return None


def process_string(s):
    s = re.sub(r'[^a-zA-Z\s]', ' ', s)
    s = re.sub(r'\s{2,}', ' ', s)
    words = s.split()
    words = [word for word in words if word.lower() not in remove_words]
    return ' '.join(words)


def get_first_500_chars(input_string):
    return input_string[:500]


def check_permissions(input_list):
    result = []
    for item in pm:
        if item in input_list:
            result.append(1)
        else:
            result.append(0)

    if any(item not in pm for item in input_list):
        result = [1] + result
    else:
        result = [0] + result

    return result


def get_md5(a):
    certs = set(a.get_certificates_der_v2() + [a.get_certificate_der(x) for x in a.get_signature_names()])
    md5_values = []
    for cert in certs:
        cert_md5 = hashlib.md5(cert).hexdigest()
        md5_values.append(cert_md5)
    return md5_values


def append(file_name, *args):
    with open(file_name, "a") as file:
        for content in args:
            file.write(str(content) + "\n")

def save_apk(apk_data):  # -> str save_path
    create_directory_if_not_exists(APK_SAVE_PATH)

    save_path =os.path.join(APK_SAVE_PATH,'temp.apk')
    with open(save_path, "wb") as f:
        f.write(apk_data)
    return save_path


class my_APK:
    def __init__(self, apk_path):
        self.a, self.d, self.dx = AnalyzeAPK(apk_path)
        self.apk_path = apk_path
        self.icon_save_path = os.path.join('temp','icon')
        self.default_icon_path = os.path.join('assets','invalid_image.png')

    def get_icon_searching(self, target_path=os.path.join("temp","icon")):
        a = self.a
        file_list = a.get_files()
        output_dir = target_path
        icon_path = None
        for file in file_list:
            if 'icon' not in file.lower():
                continue
            if file.endswith(".png") or file.endswith(".jpg"):
                icon_data = a.get_file(file)
                with open(os.path.join(target_path,'temp.png'), "wb") as f:
                    f.write(icon_data)
                icon_path = os.path.join(target_path,'temp.png')
                if 'app_icon' in file.lower():
                    break
        return icon_path

    def extract_icon_from_apk(self, icon_path):  # -> image_data or None
        with zipfile.ZipFile(self.apk_path, 'r') as zip_ref:
            # 从 APK 文件中读取图标数据
            with zip_ref.open(icon_path) as icon_file:
                # 读取图标数据
                icon_data = icon_file.read()
            if icon_path.endswith('.xml'):
                print("Icon is in XML format. Returning default image.")
                return None  #图标文件为xml文件 返回空值，表示无效的图标
            else:
                return icon_data

    def get_icon(self, target_path: str = 'None',
                 target_name: str = 'temp',
                 image: bool = False):  # -> str image_path

        if target_path == 'None':  #使用默认的目标地址
            target_path = self.icon_save_path

        icon_path = self.a.get_app_icon()
        icon_data = self.extract_icon_from_apk(icon_path)
        if icon_data is None:  #无效图片数据,搜索文件或返回默认图片地址
            icon_path = self.get_icon_searching()
            if icon_path is None:
                return self.default_icon_path
            return icon_path

        if image:  #直接返回图片数据
            return icon_data
        # 将图标数据写入目标文件地址
        create_directory_if_not_exists(target_path)
        with open( os.path.join(target_path ,target_name + ".png"), "wb") as f:
            f.write(icon_data)
        return os.path.join(target_path ,target_name + ".png")

    def get_permissions_report(self):  # -> DataFrame
        permissions = self.a.get_details_permissions()

        p = []
        for key, value in permissions.items():
            for i in range(len(value)):
                value[i] = value[i].replace('\n', '')
                value[i] = ' '.join(value[i].split())
            p.append([key] + value)

        df = pd.DataFrame(p, columns=['Name', 'Security', 'Function', 'Description'])
        columns = ['Name', 'Security', 'Function', 'Description']
        df = df[columns]
        return df

    def get_app_name(self):
        return self.a.get_app_name()

    # str

    def get_permissions(self):
        return self.a.get_permissions()

    # list

    def get_details_permissions(self):  # -> list
        return self.a.get_details_permissions()

    def get_package(self):
        return self.a.get_package()

    # str

    def get_androidversion_name(self):
        return self.a.get_androidversion_name()

    # str

    def get_androidversion_code(self):
        return self.a.get_androidversion_code()

    # str

    def get_signature_names(self):
        return self.a.get_signature_names()

    # list

    def get_android_manifest_axml(self):
        return self.a.get_android_manifest_axml()

    # <class 'androguard.core.axml.AXMLPrinter'>

    def get_activities(self):
        return self.a.get_activities()

    # list

    def get_receivers(self):
        return self.a.get_receivers()

    # list

    def get_services(self):
        return self.a.get_services()

    # list

    def get_main_activity(self):
        return self.a.get_main_activity()

    # str

    def get_providers(self):
        return self.a.get_providers()

    # list

    def get_min_sdk_version(self):  # -> list
        return self.a.get_min_sdk_version()

    def get_max_sdk_version(self):  # -> list
        return self.a.get_max_sdk_version()

    def get_score(self):  # -> str 检测结果
        return '?'

    def get_instructions(self):
        all_instructions_concatenated = ""

        # 假设 self.dx.get_methods() 返回包含 MethodAnalysis 对象的列表
        methods = self.dx.get_methods()

        for method in methods:
            # 假设 method.get_basic_blocks() 返回包含 DEXBasicBlock 对象的列表
            basic_blocks = method.get_basic_blocks()

            for block in basic_blocks:
                instructions = block.get_instructions()

                if instructions:
                    for instruction in instructions:
                        instruction_str = str(instruction)
                        instruction_str_encoded = instruction_str.encode('gbk', errors='ignore').decode('gbk',
                                                                                                        errors='ignore')
                        all_instructions_concatenated += instruction_str_encoded + " "

        # 使用正则表达式替换非字母和空白字符
        all_instructions_concatenated = re.sub(r'[^a-zA-Z\s]', ' ', all_instructions_concatenated)

        return all_instructions_concatenated

    def get_classes(self):
        classes_analysis = self.dx.get_classes()
        return classes_analysis

    # dict_values
    def get_methods(self):
        methods_generator = self.dx.get_methods()

        return list(methods_generator)

    # 返回一个list类型

    def get_strings(self):
        return self.d[0].get_strings()

    # list
    def get_fields(self):
        fields = self.dx.get_fields()

        return list(fields)

    # list
    def get_cn(self):
        package_name = self.a.get_app_name()
        all_strings = set(self.get_strings())
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
        chinese_strings = [s for s in all_strings if chinese_pattern.match(s)]
        chinese_strings.insert(0, f"{package_name}:")

        return chinese_strings

    # list
    def get_url(self):
        package_name = self.a.get_app_name()
        all_strings = set(self.get_strings())
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = [s for s in all_strings if url_pattern.match(s)]
        urls.insert(0, f"{package_name}:")
        return urls

    # list
    def get_md5(self):
        certs = set(
            self.a.get_certificates_der_v2() + [self.a.get_certificate_der(x) for x in self.a.get_signature_names()])
        md5_values = []
        for cert in certs:
            cert_md5 = hashlib.md5(cert).hexdigest()
            md5_values.append(cert_md5)
        return md5_values

    # list
    def get_info(self):
        a = check_permissions(self.a.get_permissions())
        b = int(self.a.get_androidversion_code())
        a = [b] + a
        return a

    def get_five_info(self):
        text = ""
        text += self.get_app_name() + " "
        text += process_string(str(self.get_permissions())) + " "
        text += process_string(str(self.get_package())) + " "
        text += process_string(str(self.get_androidversion_name())) + " "
        text += process_string(str(self.get_signature_names())) + " "
        text += process_string(str(self.get_activities())) + " "
        text += process_string(str(self.get_main_activity())) + " "
        text += process_string(get_first_500_chars(str(self.get_services()))) + " "
        text += process_string(get_first_500_chars(str(self.get_receivers()))) + " "
        text += process_string(get_first_500_chars(str(self.get_providers()))) + " "
        text += process_string(str(self.get_android_manifest_axml())) + " "
        text += process_string(get_first_500_chars(str(self.get_instructions()))) + " "
        text += process_string(get_first_500_chars(str(self.get_classes()))) + " "
        text += process_string(get_first_500_chars(str(self.get_methods()))) + " "
        text += process_string(get_first_500_chars(str(self.get_fields())))

        return text


# list

# name <class 'str'>
# permission <class 'list'>
# package <class 'str'>
# version_name <class 'str'>
# version_code<class 'str'>
# signauture <class 'list'>
# axml <class 'androguard.core.axml.AXMLPrinter'>
# activities <class 'list'>
# receivers <class 'list'>
# services <class 'list'>
# main_activity <class 'str'>
# providers <class 'list'>
# classes <class 'dict_values'>
# methods <class 'list'>
# strings <class 'list'>
# fields <class 'list'>
# cn <class 'list'>
# url <class 'list'>
# md5 <class 'list'>
# info <class 'list'>


#db util
class namelist:
    def __init__(self):
        self.db = sqlite3.connect("allow_deny.db")
        self.cu = self.db.cursor()
        self.cu.execute('''
         create table if not exists 白名单(
                ip varchar(30) ,
                url varchar(100),
                UNIQUE(url, ip)
                );
        '''
                        )

        self.cu.execute('''
        create table if not exists 黑名单(
                ip varchar(30) ,
                url varchar(100),
                UNIQUE(url, ip)
                );
                        ''')

        self.db.commit()

        self.cu.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = self.cu.fetchall()
        self.tables = [item[0] for item in self.tables]

    def add_list(self, IP, url, option):
        if option not in self.tables:
            return -1

        try:
            self.cu.execute(f"INSERT INTO {option} (ip, url) VALUES (?, ?)", (IP, url))
            self.db.commit()
            return 1
        except Exception as e:
            print(f"Error inserting data: {e}")
            return 0

    def get_list(self, option):
        self.cu.execute(f"select * from {option};")
        list = pd.DataFrame(self.cu.fetchall(), columns=['ip', 'url'])
        return list

    def show_tables(self):
        return self.tables

    def add_tables(self, option):
        self.cu.execute(f'''
                create table if not exists {option}(
                ip varchar(30) ,
                url varchar(100),
                UNIQUE(url, ip)
                );
                '''
                        )
        self.tables += [option]
        self.db.commit()
        pass

    def drop_tables(self, option):
        if option not in self.tables:
            return False

        self.cu.execute(f'''
                            drop table if exists{option} 
                            '''
                        )
        self.tables.remove(option)
        self.db.commit()
        return True

    def search_list(self, option, ip=None, url=None):
        if ip and url:
            self.cu.execute(
                f'''
                SELECT * FROM {option} WHERE ip = ? and url=?
                ''', (ip, url)
            )

        if ip and not url:
            self.cu.execute(
                f'''
                SELECT * FROM {option} WHERE ip = ?
                ''', (ip,)
            )

        if not ip and url:
            self.cu.execute(
                f'''
                SELECT * FROM {option} WHERE url = ?
                ''', (url,)
            )

        result = self.cu.fetchone()

        if result:
            return True
        else:
            return False


#model util
class MLP(nn.Module):
    def __init__(self, input_size):
        super(MLP, self).__init__()
        self.layer1 = nn.Linear(input_size, 64)
        self.layer2 = nn.Linear(64, 32)
        self.output = nn.Linear(32, 2)  # 二分类任务

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = self.output(x)
        return x


class Predictor:
    def __init__(self, input_size=367, pth_path=os.path.join("model","mlp_model.pth")):
        self.model = MLP(input_size)
        self.checkpoint = torch.load(pth_path)
        self.model.load_state_dict(self.checkpoint['model_state_dict'])
        self.scaler = self.checkpoint['scaler']
        self.model.eval()

    def predict(self, sample):
        with torch.no_grad():
            sample = self.scaler.transform([sample])
            sample = torch.tensor(sample, dtype=torch.float32)
            output = self.model(sample)
            predicted_class = torch.argmax(output, dim=1).item()
            probabilities = F.softmax(output, dim=1)
            confidence = probabilities[0, predicted_class].item()
        return predicted_class, confidence


#url util
def get_main_domain(url):
    ext = tldextract.extract(url)
    main_domain = ext.registered_domain
    return main_domain


def get_url_id(url):
    url_bytes = url.encode("utf-8")
    url_id = base64.urlsafe_b64encode(url_bytes).decode().strip("=")
    return url_id


def check_url_with_api(url):
    try:
        headers = {
            "x-apikey": "c0d7ffa4bb65e8b388580fed496e8ae443edb8ebab4e551fe348e9442faa3ce4"
        }

        url = get_main_domain(url)
        url_id = get_url_id(url)

        url_report_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        response = requests.get(url_report_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception  as e:
        print(e)
        return None


class BertClassifier(nn.Module):
    def __init__(self, dropout=0.5):
        super(BertClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('tokenizer')
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, 5)
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):
        _, pooled_output = self.bert(input_ids=input_id, attention_mask=mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)
        return final_layer


class url_check:
    def __init__(self, checkpoint_path=os.path.join('model','bert_model.pth')):
        self.tokenizer = BertTokenizer.from_pretrained('tokenizer')
        self.model = BertClassifier()

        if torch.cuda.is_available():
            self.state_dict = torch.load(checkpoint_path)
        else:
            self.state_dict = torch.load(checkpoint_path, map_location=torch.device('cpu'))

        self.state_dict = {k: v for k, v in self.state_dict.items() if k in self.model.state_dict()}

        self.model.load_state_dict(self.state_dict, strict=False)

        self.model.eval()

        use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if use_cuda else "cpu")
        if use_cuda:
            self.model = self.model.cuda()

    def predict(self, text):
        text = get_main_domain(text)
        encoding = self.tokenizer(text, padding='max_length', max_length=64, truncation=True, return_tensors="pt")
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            output = self.model(input_ids, attention_mask)

        predicted_class = output.argmax(dim=1).item()
        return predicted_class


#util download
curdir = os.getcwd()  # 获取当前路径current work directory

data_dir = os.path.join(curdir, r"temp\data")


def check_url(url, page_url):
    if not url.startswith('http'):
        url = page_url + url
        return url


# 创建文件夹
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def check_for_apk(directory=data_dir):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.apk'):
                return 1
    return -1


def get_redirected_url(url, page_url):
    try:
        if not url.startswith('http'):
            url = page_url + url
        response = requests.head(url, allow_redirects=True)
        redirected_url = response.url
        return redirected_url
    except requests.RequestException as e:
        print("Error:", e)
        return None


def get_static_links(url):
    # 发送GET请求获取页面内容
    response = requests.get(url)
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # 找到所有的<a>标签
    links = soup.find_all('a')
    # 提取链接
    all_links = [link.get('href') for link in links if link.get('href')]

    return all_links


def get_dynamic_links(url):
    # 使用Selenium模拟浏览器行为
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # 无头模式
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # 提取动态加载后的链接
    dynamic_links = driver.execute_script(
        'return [].map.call(document.querySelectorAll("a"), function(link) { return link.href; })')

    driver.quit()

    return dynamic_links


def get_all_links(url):
    static_links = get_static_links(url)
    dynamic_links = get_dynamic_links(url)
    all_links = static_links + dynamic_links
    for i in range(len(all_links)):
        if not all_links[i].startswith('http'):
            all_links[i] = urljoin(url, all_links[i])
    apk_links = []
    for link in all_links:
        if is_apk_url(link):
            apk_links.append(link)
        else:
            redirected_url = get_redirected_url(link, url)  # 传递page_url参数
            if redirected_url and is_apk_url(redirected_url):
                apk_links.append(redirected_url)

    return apk_links


def is_apk_url(url):
    if url.endswith('.apk'):
        return True
    else:
        try:
            response = requests.head(url)
            content_type = response.headers.get('Content-Type')

            if content_type == 'application/vnd.android.package-archive':
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return False


def get_qrcode(image_binary):
    print("调用二维码函数成功！")
    nparr = np.frombuffer(image_binary, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    decoded_objects = decode(img)
    for obj in decoded_objects:
        if obj.type == 'QRCODE':
            return obj.data.decode('GBK')
    return None


def generate_header():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
        'Date': current_time,
    }
    return header


def sanitize_and_validate_filename(filename):
    cleaned_filename = filename.split('?')[0]
    sanitized_filename = "".join(c for c in cleaned_filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
    if not sanitized_filename.endswith('.apk'):
        sanitized_filename += '.apk'
    return sanitized_filename


def download_single_apk(apk_url, progress_callback=None):
    if is_apk_url(apk_url) == False:
        return -1
    print(apk_url)

    save_path = sanitize_and_validate_filename(os.path.basename(apk_url))
    save_path = os.path.join(data_dir, save_path)

    try:
        with requests.get(apk_url, headers=generate_header(), allow_redirects=True, timeout=180, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            chunk_size = 1024
            downloaded_size = 0

            with open(save_path, "wb") as hf:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        hf.write(chunk)
                        downloaded_size += len(chunk)
                        progress = downloaded_size / total_size * 100
                        st.session_state['progress'] = progress / 100
                        if progress_callback:
                            progress_callback()
                        print(f"\r正在下载中: {progress:.2f}%", end="")

        print("\n下载完成！")
        return 0
    except Exception as e:
        print("发生错误,无法下载APK")
        print(e)
        return -1


def sliding_window_tokenizer(text, tokenizer, max_length=128, stride=64):
    encoding = tokenizer(text, return_tensors='pt', truncation=False)  # 对文本进行编码
    input_ids = encoding['input_ids'].squeeze(0)  # 获取input_ids并去除批次维度
    attention_mask = encoding['attention_mask'].squeeze(0)  # 获取attention_mask并去除批次维度

    token_windows = []  # 初始化存储token窗口的列表
    for i in range(0, len(input_ids), stride):  # 按照步长进行滑动窗口
        window_input_ids = input_ids[i:i + max_length]  # 获取当前窗口的input_ids
        window_attention_mask = attention_mask[i:i + max_length]  # 获取当前窗口的attention_mask

        if len(window_input_ids) < max_length:  # 如果当前窗口的长度小于最大长度
            pad_length = max_length - len(window_input_ids)  # 计算需要填充的长度
            window_input_ids = torch.cat([window_input_ids, torch.zeros(pad_length, dtype=torch.long)])  # 填充input_ids
            window_attention_mask = torch.cat(
                [window_attention_mask, torch.zeros(pad_length, dtype=torch.long)])  # 填充attention_mask

        token_windows.append((window_input_ids, window_attention_mask))  # 将当前窗口加入列表

    return token_windows  # 返回所有的token窗口


# 定义Bert分类器类
class BertClassifier5(nn.Module):
    def __init__(self, dropout=0.5):
        super(BertClassifier5, self).__init__()
        self.bert = BertModel.from_pretrained('tokenizer')  # 加载预训练的BertModel
        self.dropout = nn.Dropout(dropout)  # 定义dropout层
        self.linear = nn.Linear(768, 5)  # 定义线性层，输出维度为5

    def forward(self, input_ids, attention_mask):
        num_windows, seq_len = input_ids.size()  # 获取batch的大小，窗口数量和序列长度
        input_ids = input_ids.view(-1, seq_len)  # 将input_ids展平
        attention_mask = attention_mask.view(-1, seq_len)  # 将attention_mask展平

        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)  # 获取Bert的输出
        pooled_output = outputs.pooler_output  # 获取池化输出
        pooled_output = pooled_output.view(1, num_windows, -1).mean(dim=1)  # 对窗口进行平均池化

        dropout_output = self.dropout(pooled_output)  # 通过dropout层
        linear_output = self.linear(dropout_output)  # 通过线性层
        return linear_output  # 返回输出


# 定义加载检查点函数
def load_checkpoint(model):
    if os.path.exists(CHECKPOINT_FILE):  # 检查检查点文件是否存在
        checkpoint = torch.load(CHECKPOINT_FILE, map_location=torch.device('cpu'))  # 加载检查点，使用CPU
        if torch.cuda.is_available():
            checkpoint = torch.load(CHECKPOINT_FILE)
        else:
            checkpoint = torch.load(CHECKPOINT_FILE, map_location=torch.device('cpu'))
        model_state_dict = checkpoint['model_state_dict']  # 获取模型状态字典
        if isinstance(model, nn.DataParallel):
            model.module.load_state_dict(model_state_dict)  # 加载模型状态字典
        else:
            model.load_state_dict(model_state_dict)
        print("Checkpoint loaded.")
    else:
        print("No checkpoint found.")


# 定义用于预测的类
class Five_Bert:
    def __init__(self):
        self.model = BertClassifier5()  # 实例化模型
        self.use_cuda = torch.cuda.is_available()  # 检查是否可以使用CUDA
        self.device = torch.device("cuda" if self.use_cuda else "cpu")
        print(self.device)
        load_checkpoint(self.model)  # 加载预训练模型
        self.tokenizer = BertTokenizer.from_pretrained('tokenizer')

        # 设置设备为GPU或CPU
        self.model.to(self.device)  # 将模型移动到设备
        if self.use_cuda:
            self.model = nn.DataParallel(self.model).cuda()
        self.model.eval()

    def predict(self, text):
        token_windows = sliding_window_tokenizer(text, self.tokenizer)  # 对输入文本进行滑动窗口分词
        input_ids_list, attention_mask_list = zip(*token_windows)  # 解压得到input_ids和attention_mask列表

        input_ids = torch.stack(input_ids_list).to(self.device)  # 将input_ids堆叠成张量并移动到设备
        attention_mask = torch.stack(attention_mask_list).to(self.device)
        with torch.no_grad():  # 不进行梯度计算
            output = self.model(input_ids, attention_mask)  # 通过模型获取输出
            pred = output.argmax(dim=1).item()  # 获取预测结果

        predicted_label = id_to_label[pred]  # 获取预测标签
        return predicted_label


def download_apk(method_code=1, url=None, qrcode=None, progress_callback=None):
    apk_num = 1
    success_num = 0

    def download_and_count(urls):
        nonlocal apk_num, success_num
        if isinstance(urls, str):
            urls = [urls]
        apk_num = len(urls)
        for apk_url in urls:
            if is_apk_url(apk_url):
                b = download_single_apk(apk_url, progress_callback)
                if b == 1:
                    success_num += 1
        return apk_num, success_num

    if method_code == 1:
        if is_apk_url(url):
            download_single_apk(url, progress_callback)
            return apk_num, 1
        else:
            return apk_num, 0

    elif method_code == 2:
        urls = get_qrcode(qrcode)
        print(urls)
        if not urls:
            return apk_num, 0
        download_single_apk(urls, progress_callback)
        return apk_num,1

    elif method_code == 3:
        urls = get_all_links(url)
        return download_and_count(urls)

    else:
        return apk_num, 0
