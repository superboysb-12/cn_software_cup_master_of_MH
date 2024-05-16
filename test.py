import util
from androguard.misc import AnalyzeAPK
import os
import datetime


apk_folder = "..\dataset\sex\sex"
current_time = datetime.datetime.now()
file_name = 'apk_md5_values'
with open(file_name, "w"):
    pass

for filename in os.listdir(apk_folder):
    if filename.endswith(".apk"):
        apk_path = os.path.join(apk_folder, filename)

        a, d, dx = AnalyzeAPK(apk_path)

    util.append(file_name,util.get_md5(a))