from url import Get_Url
import os
import datetime
import util


apk_folder = "..\dataset\sex\sex"
current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") +" urls" +".txt"
with open(file_name, "w"):
    pass

for filename in os.listdir(apk_folder):
    if filename.endswith(".apk"):
        apk_path = os.path.join(apk_folder, filename)

        urls=Get_Url(apk_path)
        for url in urls:
            util.append(file_name,url)


