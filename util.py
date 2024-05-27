import hashlib
import re
import cv2
from pyzbar.pyzbar import decode
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.analysis import analysis


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

def append(file_name, *args):
    with open(file_name, "a") as file:
        for content in args:
            file.write(str(content) + "\n")

class my_APK:
    def __init__(self, apk_path):
        self.a = APK(apk_path)
        self.d = DalvikVMFormat(self.a.get_dex())
        self.dx = analysis.Analysis(self.d)

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

    def get_android_manifest_axml(self):
        return self.a.get_android_manifest_axml()

    def get_activities(self):
        return self.a.get_activities()

    def get_receivers(self):
        return self.a.get_receivers()

    def get_services(self):
        return self.a.get_services()

    def get_main_activity(self):
        return self.a.get_main_activity()

    def get_providers(self):
        return self.a.get_providers()

    def get_instructions(self):

        all_instructions_concatenated = ""
        for method in self.d.get_methods():
            instructions = method.get_instructions()
            if instructions:
                for instruction in instructions:
                    all_instructions_concatenated += str(instruction) + " "

        return all_instructions_concatenated

    def get_classes(self):
        classes_analysis = self.dx.get_classes()
        class_names = [class_analysis.get_vm_class().get_name() for class_analysis in classes_analysis]
        return class_names

    def get_methods(self):
        methods_generator = self.dx.get_methods()
        method_names = [method.get_method().get_name() for method in methods_generator]
        return method_names

    def get_strings(self):
        return self.dx.get_strings()


    def get_fields(self):
        return self.d.get_fields()

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
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
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
