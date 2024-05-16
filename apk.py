import os
import datetime
from androguard.misc import AnalyzeAPK
import util

# 定义 APK 文件夹路径
apk_folder = "..\dataset\sex\sex"
current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
with open(file_name, "w"):
    pass

for filename in os.listdir(apk_folder):
    if filename.endswith(".apk"):
        apk_path = os.path.join(apk_folder, filename)

        a, d, dx = AnalyzeAPK(apk_path)

        print("APK 应用名称:", a.get_app_name())
        print("APK 使用权限:",a.get_permissions())
        print("包名 (Package Name):", a.get_package())
        print("版本名 (Version Name):", a.get_androidversion_name())
        print("版本号 (Version Code):", a.get_androidversion_code())
        print("应用签名 (App Signature):", a.get_signature_names())
        print("APK MD5值", util.get_md5(a))

        util.append(file_name,a.get_app_name(),a.get_permissions(),a.get_package(),a.get_androidversion_name(),a.get_androidversion_code(),a.get_signature_names(),util.get_md5(a))



