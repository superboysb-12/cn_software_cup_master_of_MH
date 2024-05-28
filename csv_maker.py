import csv
import os
import datetime
from util import my_APK

# Get current time and generate file names
current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S")
limited_file_name = file_name + "_limited.csv"
full_file_name = file_name + "_full.csv"
error_file_name = file_name + "_errors.csv"

# Define the maximum number of characters for each column
MAX_CHARS_PER_COLUMN = 500


# Function to truncate text to a maximum number of characters
def truncate_text(text):
    return text[:MAX_CHARS_PER_COLUMN]


# Process APK files
apk_folder = "../datasets"
with open(limited_file_name, "w", newline='', encoding='gbk', errors='ignore') as limited_csvfile, \
        open(full_file_name, "w", newline='', encoding='gbk', errors='ignore') as full_csvfile, \
        open(error_file_name, "w", newline='', encoding='gbk', errors='ignore') as errorfile:
    limited_writer = csv.writer(limited_csvfile)
    full_writer = csv.writer(full_csvfile)
    error_writer = csv.writer(errorfile)
    limited_writer.writerow(
        ["label", "name", "permissions", "packagename", "version", "signature", "activity", "main_activities",
         "service", "receivers", "providers", "manifest", "instruction", "classes", "method", "field"])
    full_writer.writerow(
        ["label", "name", "permissions", "packagename", "version", "signature", "activity", "main_activities",
         "service", "receivers", "providers", "manifest", "instruction", "classes", "method", "field"])

    for dirname in os.listdir(apk_folder):
        path_dir = os.path.join(apk_folder, dirname)
        for apk_name in os.listdir(path_dir):
            apk_path = os.path.join(path_dir, apk_name)
            try:
                apk_instance = my_APK(apk_path)


                # Truncate each column to the maximum number of characters
                truncated_data = [
                    truncate_text(dirname),
                    truncate_text(apk_instance.get_app_name()),
                    truncate_text(apk_instance.get_permissions()),
                    truncate_text(apk_instance.get_package()),
                    truncate_text(apk_instance.get_androidversion_name()),
                    truncate_text(apk_instance.get_signature_names()),
                    truncate_text(apk_instance.get_activities()),
                    truncate_text(apk_instance.get_main_activity()),
                    truncate_text(apk_instance.get_services()),
                    truncate_text(apk_instance.get_receivers()),
                    truncate_text(apk_instance.get_providers()),
                    truncate_text(apk_instance.get_android_manifest_axml()),
                    truncate_text(apk_instance.get_instructions()),
                    truncate_text(apk_instance.get_classes()),
                    truncate_text(apk_instance.get_methods()),
                    truncate_text(apk_instance.get_fields())
                ]
                limited_writer.writerow(truncated_data)
                full_writer.writerow([
                    dirname,
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
                ])
                print("已经完成一次写入！")
            except Exception as e:
                error_writer.writerow([apk_path, repr(e)])
