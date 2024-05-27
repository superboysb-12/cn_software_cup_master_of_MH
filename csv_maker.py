import csv
import os
import datetime
from util import my_APK

# Get current time and generate file names
current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
error_file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + "_errors.csv"

# Open CSV files
with open(file_name, "w", newline='', encoding='gbk', errors='ignore') as csvfile, \
     open(error_file_name, "w", newline='', encoding='gbk', errors='ignore') as errorfile:
    writer = csv.writer(csvfile)
    error_writer = csv.writer(errorfile)
    writer.writerow(["name", "permissions", "packagename", "version", "signature", "activity", "main_activities",
                     "service", "receivers", "providers", "manifest", "instruction", "classes", "method", "field"])

    # Process APK files
    apk_folder = "../dataset/test1"
    for dirname in os.listdir(apk_folder):
        path_dir = os.path.join(apk_folder, dirname)
        for apk_name in os.listdir(path_dir):
            apk_path = os.path.join(path_dir, apk_name)
            try:
                apk_instance = my_APK(apk_path)
                data = [
                    apk_instance.get_app_name(),
                    apk_instance.get_permissions(),
                    apk_instance.get_package(),
                    apk_instance.get_androidversion_name(),
                    apk_instance.get_signature_names(),
                    apk_instance.get_activities(),
                    apk_instance.get_main_activity(),
                    apk_instance.get_services(),
                    apk_instance.get_receivers(),
                    apk_instance.get_providers(),
                    apk_instance.get_android_manifest_axml(),
                    apk_instance.get_instructions(),
                    apk_instance.get_classes(),
                    apk_instance.get_methods(),
                    apk_instance.get_fields()
                ]
                if any(data):
                    writer.writerow(data)
            except Exception as e:
                error_writer.writerow([apk_path, repr(e)])
