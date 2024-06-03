from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.adb_device import AdbDeviceTcp


def start_dynamic_analysis():
    # 指定公钥和私钥的路径
    adbkey_path = 'D:/AndoridAVD/.android/adbkey'

    # 使用PythonRSASigner加载公钥和私钥
    with open(adbkey_path, 'rb') as f:
        priv = f.read()
    with open(adbkey_path + '.pub', 'rb') as f:
        pub = f.read()
    signer = PythonRSASigner(pub, priv)

    # 返回signer以供后续使用
    return signer


import subprocess


def start_emulator(emulator_name):
    # 启动模拟器的命令
    start_cmd = ['emulator', '-avd', emulator_name]

    # 在后台启动模拟器
    subprocess.Popen(start_cmd)

def link_to_device(signer):

    # 设备的IP地址和端口
    device = AdbDeviceTcp('127.0.0.1', 5555, default_transport_timeout_s=9.)
    device.connect(rsa_keys=[signer], auth_timeout_s=0.1)

    # 返回device以供后续使用
    return device

def install_APK(apk_path):
    # 获取设备序列号
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    devices = result.stdout.splitlines()
    serial = None
    for line in devices[1:]:
        if 'device' in line:
            serial = line.split('\t')[0]
            break

    if serial:
        # 构建ADB安装命令
        cmd = ['adb', '-s', serial, 'install', apk_path]

        # 执行命令并打印状态消息
        print("正在安装")
        subprocess.run(cmd, check=True)
        print("安装完毕")
    else:
        print("没有找到设备")

def start_APK(device):
    # 启动APK
    package_name = 'com.tencent.mobileqq'
    main_activity = 'com.tencent.mobileqq.activity.SplashActivity'
    device.shell(f'am start -n {package_name}/{main_activity}')

def run_APK(device):
    # 模拟点击和发送按键事件
    device.shell('input tap x y')  # 替换为实际的坐标值
    device.shell('input keyevent KEYCODE_MENU')


def catch_APK(device):
    # 开始抓包
    device.shell('tcpdump -i any -w /sdcard/capture.pcap')  # 确保设备已root并安装了tcpdump


# 使用示例
signer = start_dynamic_analysis()
start_emulator('Emulator')
device = link_to_device(signer)
apk_path = "D:/ADS/dataset/test1/test01/QQ.apk"
#install_APK(apk_path)
start_APK(device)
run_APK(device)
catch_APK(device)

