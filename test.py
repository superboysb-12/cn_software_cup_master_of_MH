import util
from androguard.misc import AnalyzeAPK

apk_path = "..\dataset\sex\sex\lm.apk"

a, d, dx = AnalyzeAPK(apk_path)

print("APK MD5值", util.get_md5(a))

