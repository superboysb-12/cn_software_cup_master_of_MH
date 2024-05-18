from get_cn import Get_Cn
import os
import datetime
import util


apk_folder = "..\dataset\sex\sex"
current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") +" zh" +".txt"
with open(file_name, "w"):
    pass
for filename in os.listdir(apk_folder):
    if filename.endswith(".apk"):
        apk_path = os.path.join(apk_folder, filename)

        cns=Get_Cn(apk_path)
        util.append(file_name,cns[0])
        util.append(file_name, " ".join(cns[1:]))
