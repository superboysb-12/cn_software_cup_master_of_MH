from url import Get_Url
import os
import datetime
import util
from androguard.misc import AnalyzeAPK

apk_folder = "..\dataset\sex\sex"
current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") +" urls" +".txt"
with open(file_name, "w"):
    pass

for filename in os.listdir(apk_folder):
    if filename.endswith(".apk"):
        apk_path = os.path.join(apk_folder, filename)
        a, d, dx = AnalyzeAPK(apk_path)
        urls=Get_Url(a,d)
        for url in urls:
            util.append(file_name,url)


