import csv
import os
import datetime
from util import APK

current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

def check_non_empty(*args):
    for string in args:
        if string:
            return 1
    return 0


with open(file_name, "w",newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["name", "permissions", "get_package","version_name","signature","type"])
    pass

apk_folder = "..\dataset\\test"

for dirname in os.listdir(apk_folder):
    path_dir=apk_folder+"\\"+dirname
    for apk_name in os.listdir(path_dir):
        apk_path=path_dir+"\\"+apk_name
        apk = APK(apk_path)
        with open(file_name, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            name=apk.get_app_name()
            permissions=apk.get_permissions()
            packagename=apk.get_package()
            version=apk.get_androidversion_code()
            signature=apk.get_signature_names()

            if check_non_empty(name,permissions,packagename,version,signature):
                writer.writerow([name,permissions,packagename,version,signature,dirname])


