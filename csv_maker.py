import csv
import os
import datetime
from util import APK
from androguard.core.axml import ResParserError

# 获取当前时间并生成文件名
current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
error_file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + "_errors.csv"

# 检查是否有非空字符串
def check_non_empty(*args):
    for string in args:
        if string:
            return True
    return False

# 创建CSV文件并写入表头
with open(file_name, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["name", "permissions", "get_package", "version_name", "signature", "type"])

# 创建错误日志CSV文件并写入表头
with open(error_file_name, "w", newline='') as errorfile:
    error_writer = csv.writer(errorfile)
    error_writer.writerow(["apk_path", "error"])

# APK文件夹路径
apk_folder = "..\\dataset\\datasets"

# 遍历APK文件夹
for dirname in os.listdir(apk_folder):
    path_dir = os.path.join(apk_folder, dirname)
    for apk_name in os.listdir(path_dir):
        apk_path = os.path.join(path_dir, apk_name)
        try:
            apk = APK(apk_path)
        except Exception as e:
            with open(error_file_name, "a", newline='') as errorfile:
                error_writer = csv.writer(errorfile)
                error_writer.writerow([apk_path, str(e)])
            continue

        with open(file_name, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            try:
                name = apk.get_app_name()
                permissions = apk.get_permissions()
                packagename = apk.get_package()
                version = apk.get_androidversion_code()
                signature = apk.get_signature_names()

                if check_non_empty(name, permissions, packagename, version, signature):
                    writer.writerow([name, permissions, packagename, version, signature, dirname])
            except Exception as e:
                with open(error_file_name, "a", newline='') as errorfile:
                    error_writer = csv.writer(errorfile)
                    error_writer.writerow([apk_path, str(e)])
                continue
