import hashlib
import re
from androguard.misc import AnalyzeAPK
import zipfile
from datetime import datetime
import pandas as pd
from androguard.util import set_log
set_log("ERROR")#set log message only ERROR
import sqlite3

APK_SAVE_PATH = r"temp\apk"



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
      'android.permission.sec.MDM_SECURITY', 'android.permission.status_bar']


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

def save_apk(apk_data): # -> str save_path
    current_time = datetime.now()
    time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    save_path = APK_SAVE_PATH +'\\'+''.join([c for c in time if c != ':' and c != '-' and c != ' ' ])+r".apk"
    with open(save_path, "wb") as f:
        f.write(apk_data)
    return save_path


class my_APK:
    def __init__(self, apk_path):
        self.a ,self.d,self.dx= AnalyzeAPK(apk_path)
        self.apk_path = apk_path
        self.icon_save_path = r"temp\icon"
        self.default_icon_path = r"assets\invalid_image.png"

    def extract_icon_from_apk(self, icon_path): # -> image_data or None
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

    def get_icon(self,target_path: str = 'None',
                 target_name: str = 'None',
                 image: bool = True):# -> str image_path

        if target_path == 'None':#使用默认的目标地址
            target_path = self.icon_save_path

        icon_path = self.a.get_app_icon()
        icon_data = self.extract_icon_from_apk(icon_path)
        if icon_data is None:#无效图片数据,返回默认图片地址
            return self.default_icon_path

        if image:#直接返回图片数据
            return icon_data
        # 将图标数据写入目标文件地址
        with open(target_path + '\\' + target_name + ".png", "wb") as f:
            f.write(icon_data)
        return target_path + '\\' + target_name + ".png"

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

    def get_details_permissions(self): # -> list
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

    def get_min_sdk_version(self): # -> list
        return self.a.get_min_sdk_version()

    def get_max_sdk_version(self): # -> list
        return self.a.get_max_sdk_version()

    def get_score(self): # -> str 检测结果
        return '?'


    # def get_instructions(self):
    #     all_instructions_concatenated = ""
    #     for method in self.dx.get_methods():
    #         instructions = method.get_instructions()
    #         if instructions:
    #             for instruction in instructions:
    #                 instruction_str = str(instruction)
    #                 instruction_str_encoded = instruction_str.encode('gbk', errors='ignore').decode('gbk',
    #                                                                                                 errors='ignore')
    #                 all_instructions_concatenated += instruction_str_encoded + " "
    #
    #     all_instructions_concatenated = re.sub(r'[^a-zA-Z\s]', ' ', all_instructions_concatenated)
    #
    #     return all_instructions_concatenated

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



class namelist:
    def __init__(self):
        self.db = sqlite3.connect("allow_deny.db")
        self.cu=self.db.cursor()
        self.cu = self.db.cursor()
        self.cu.execute('''
        create table if not exists 白名单(
        ip varchar(30) primary key
        );
        '''
        )

        self.cu.execute('''
        create table if not exists 白名单(
        ip varchar(30) primary key
        );
        '''
        )

        self.db.commit()

        self.cu.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = self.cu.fetchall()
        self.tables = [item[0] for item in self.tables]

    def add_list(self,IP, option):
        if option=='白名单' or option=='黑名单':
            return -1

        if option not in self.tables:
            return -1
        self.cu.execute(f"insert into {option} (ip) values (?)", (IP,))
        self.db.commit()
        return 1

    def get_allow_list(self):
        self.cu.execute("select * from 白名单;")
        allowlist = pd.DataFrame(self.cu.fetchall(), columns=['ip'])
        return allowlist

    def get_deny_list(self):
        self.cu.execute("select * from 黑名单;")
        denylist = pd.DataFrame(self.cu.fetchall(), columns=['ip'])
        return denylist

    def show_tables(self):
        return self.tables



    def add_tables(self,option):
        self.cu.execute(f'''
                create table if not exists {option}(
                ip varchar(30) primary key
                );
                '''
                        )
        self.tables+=[option]
        pass