import hashlib
from androguard.misc import AnalyzeAPK
import re
import cv2
from pyzbar.pyzbar import decode

def get_qrcode(image_path):
    img = cv2.imread(image_path)
    decoded_objects = decode(img)
    return decoded_objects

def get_md5(a):
    certs = set(a.get_certificates_der_v2() + [a.get_certificate_der(x) for x in a.get_signature_names()])
    md5_values = []
    for cert in certs:
        cert_md5 = hashlib.md5(cert).hexdigest()
        md5_values.append(cert_md5)
    return md5_values

def append(file_name,*args):
    with open(file_name, "a") as file:
        for content in args:
            file.write(str(content) + "\n")

class APK:
    def __init__(self, apk_path):
        self.a, self.d, self.dx = AnalyzeAPK(apk_path)

    def get_app_name(self):
        return self.a.get_app_name()

    def get_permissions(self):
        return self.a.get_permissions()

    def get_package(self):
        return self.a.get_package()

    def get_androidversion_name(self):
        return self.a.get_androidversion_name()

    def get_androidversion_code(self):
        return self.a.get_androidversion_code()

    def get_signature_names(self):
        return self.a.get_signature_names()

    def get_cn(self):
        package_name = self.a.get_app_name()
        all_strings = set(self.d[0].get_strings())
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
        chinese_strings = [s for s in all_strings if chinese_pattern.match(s)]
        chinese_strings.insert(0, f"{package_name}:")

        return chinese_strings

    def get_url(self):
        package_name = self.a.get_app_name()
        all_strings = set(self.d[0].get_strings())
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = [s for s in all_strings if url_pattern.match(s)]
        urls.insert(0, f"{package_name}:")
        return urls

    def get_md5(self):
        certs = set(self.a.get_certificates_der_v2() + [self.a.get_certificate_der(x) for x in self.a.get_signature_names()])
        md5_values = []
        for cert in certs:
            cert_md5 = hashlib.md5(cert).hexdigest()
            md5_values.append(cert_md5)
        return md5_values

