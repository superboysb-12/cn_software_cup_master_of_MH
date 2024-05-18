import re
from androguard.misc import AnalyzeAPK


def Get_Url(apk_path):
    a, d, dx = AnalyzeAPK(apk_path)
    package_name = a.get_app_name()
    all_strings = set(d[0].get_strings())
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = [s for s in all_strings if url_pattern.match(s)]
    urls.insert(0, f"{package_name}:")

    return urls

