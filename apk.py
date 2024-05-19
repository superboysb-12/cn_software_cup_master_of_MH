import os
import datetime
from androguard.misc import AnalyzeAPK
from util import APK,append


# 定义 APK 文件夹路径
apk_folder = "..\dataset\sex\sex"
current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
with open(file_name, "w"):
    pass

for filename in os.listdir(apk_folder):
    if filename.endswith(".apk"):
        apk_path = os.path.join(apk_folder, filename)

        apk = APK(apk_path)
        '''
        print("APK 应用名称:", apk.get_app_name())
        print("APK 使用权限:",apk.get_permissions())
        print("包名 (Package Name):", apk.get_package())
        print("版本名 (Version Name):", apk.get_androidversion_name())
        print("版本号 (Version Code):", apk.get_androidversion_code())
        print("应用签名 (App Signature):", apk.get_signature_names())
        print("APK MD5值", apk.get_md5())
        '''
        cns=apk.get_cn()
        urls=apk.get_url()
        append(file_name,
               apk.get_app_name(),
               apk.get_permissions(),
               apk.get_package(),
               apk.get_androidversion_name(),
               apk.get_androidversion_code(),
               apk.get_signature_names(),
               apk.get_md5(),
               cns[0],
               " ".join(cns[1:])
               )
        for url in urls:
            append(file_name,url)



