import struct,socket
import ctypes as ct
import libpcap as pcap


errbuf = ct.create_string_buffer(pcap.PCAP_ERRBUF_SIZE + 1)
#指定抓包设备
alldevs = ct.POINTER(pcap.pcap_if_t)()
pcap.findalldevs(ct.byref(alldevs), errbuf)
for dev in alldevs:
    print(dev.name)
    device = dev.name
    break  # 使用第一个
pcap.freealldevs(alldevs)

handle = pcap.open_live(device, 4096, 1, 1000, errbuf)
if errbuf.value:
    print("hanle error :", errbuf.value)
fname = b"realtime1.cap"
fPcap = pcap.dump_open(handle, fname)
fPcapUbyte = ct.cast(fPcap, ct.POINTER(ct.c_ubyte))

pheader = pcap.pkthdr()
i = 0
print("live cap begin")
while True:
    packet = pcap.next(handle, pheader)
    if not packet: continue
    print(i, pheader.ts.tv_sec, pheader.len, pheader.caplen)
    p = ct.pointer(packet.contents)
    ipInfo = struct.unpack('<BBHHHBBH4s4s', bytes(p[14:34]))
    srcIp = socket.inet_ntoa(ipInfo[-2])
    dstIp = socket.inet_ntoa(ipInfo[-1])
    print(srcIp, "=>", dstIp)
    pcap.dump(fPcapUbyte, pheader, packet)

    i = i + 1
    if i > 10:
        break
print("i = ", i)
print("live cap end")
pcap.close(handle)  # need close
pcap.dump_flush(fPcap)
pcap.dump_close(fPcap)



#device = b'\\Device\\NPF_{434AE621-ABE6-4168-93D3-D16986E0FD0C}'  # Windows


'''from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.adb_device import AdbDeviceTcp
import subprocess
import time

apk_path = "D:/ADS/dataset/test1/test01/QQ.apk"
package_name = 'com.tencent.mobileqq'
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

def get_uid(device, package_name):
    # 使用adb命令获取应用的UID
    uid_cmd = f"dumpsys package {package_name} | grep userId"
    result = device.shell(uid_cmd)
    uid = result.split('=')[1].split()[0]
    print('uid:',uid)
    return uid

def catch_APK(device, package_name):
    # 获取应用的UID
    uid = get_uid(device, package_name)
    # 开始抓包
    device.shell(f"tcpdump -i any -w /sdcard/capture.pcap")
    print('capturing')
def start_APK(device):
    # 启动APK
    package_name = 'com.tencent.mobileqq'
    main_activity = 'com.tencent.mobileqq.activity.SplashActivity'
    device.shell(f'am start -n {package_name}/{main_activity}')
def run_APK(device):
    # 模拟点击和发送按键事件
    device.shell('input tap 100 200')  # 替换为实际的坐标值
    device.shell('input keyevent KEYCODE_MENU')

def stop_tcpdump(device):
    # 使用adb命令获取tcpdump的PID
    pid_cmd = "ps | grep tcpdump | awk '{print $2}'"
    pid = device.shell(pid_cmd)
    print('pid:',pid)
    # 使用kill命令停止tcpdump
    kill_cmd = f"kill {pid}"
    device.shell(kill_cmd)
    print('tcpdump stopped')

def pull_capture():
    pull_cmd = 'adb pull /sdcard/capture.pcap D:/ADS/cn_software_cup_master_of_MH/temp'
    subprocess.run(pull_cmd)

signer = start_dynamic_analysis()
device = link_to_device(signer)
#install_APK(apk_path)
catch_APK(device,package_name)
#start_APK(device)
#run_APK(device)
time.sleep(60)
stop_tcpdump(device)

#adb shell dumpsys package com.tencent.mobileqq |adb shell grep userId
#adb shell tcpdump -i any -w /sdcard/capture.pcap 'uid 10050'
'''