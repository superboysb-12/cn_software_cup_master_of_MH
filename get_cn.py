import re
from androguard.misc import AnalyzeAPK

def Get_Cn(apk_path):
    a, d, dx = AnalyzeAPK(apk_path)
    package_name = a.get_app_name()
    all_strings = set(d[0].get_strings())
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    chinese_strings = [s for s in all_strings if chinese_pattern.match(s)]
    chinese_strings.insert(0, f"{package_name}:")

    return chinese_strings