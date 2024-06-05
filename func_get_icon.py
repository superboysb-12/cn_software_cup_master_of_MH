from androguard.core.bytecodes.apk import APK
import zipfile

def extract_icon_from_apk(apk_path, icon_path):
    with zipfile.ZipFile(apk_path, 'r') as zip_ref:
        # 检查图标路径是否存在于 APK 文件中
        if icon_path in zip_ref.namelist():
            # 从 APK 文件中读取图标数据
            with zip_ref.open(icon_path) as icon_file:
                # 读取图标数据
                icon_data = icon_file.read()
            return icon_data
        else:
            print("Icon path not found in APK.")

def get_icon(apk_path :str , target_path :str,target_name : str):
    # 调用函数提取图标数据
    a = APK(apk_path, testzip=True)
    icon_path = a.get_app_icon()
    print(icon_path)
    icon_data = extract_icon_from_apk(apk_path, icon_path)

    # 将图标数据写入文件
    if icon_data:
        with open(target_path+'\\'+target_name+".png", "wb") as f:
            f.write(icon_data)
        print("Icon extracted and saved as app_icon.png.")
    else:
        print("Failed to extract icon.")


'''
import os

def list_files(directory):
    """
    遍历指定目录下的所有文件，并返回一个文件路径列表。
    """
    files = []
    # 遍历目录下的所有文件和子目录
    for root, _, filenames in os.walk(directory):
        # 遍历当前目录中的文件
        for filename in filenames:
            # 构造文件的完整路径
            file_path = os.path.join(root, filename)
            # 将文件路径添加到列表中
            files.append(file_path)
    return files

# 指定目录路径
directory_path = r"D:\学习资料\反炸APP分析\apk\sex\sex"
# 获取目录中的所有文件
files_list = list_files(directory_path)

i = 0
# 打印文件列表
for file_path in files_list:
    i+=1
    get_icon(file_path,r"D:\pythonProject\APKAnalysis\output",str(i))
'''
