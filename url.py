import re
from androguard.misc import AnalyzeAPK

apk_path = "..\dataset\sex\sex\lm.apk"
a, d, dx = AnalyzeAPK(apk_path)

all_strings = set()
for string in d[0].get_strings():
    all_strings.add(string)

url_pattern = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

urls = [s for s in all_strings if url_pattern.match(s)]

print("Extracted URLs:")
for url in urls:
    print(url)
