import hashlib


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
