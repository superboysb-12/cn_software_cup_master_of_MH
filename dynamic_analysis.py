import subprocess
from scapy.all import *
from time import sleep
import csv
import pandas as pd
import threading
import time
import os
'''
需要关防火墙
'''


#Local path
CAPTURE_PATH = os.path.join('temp','capture','capture.pcap')
CSV_PATH = os.path.join('temp','capture','capture.csv')
TEMP_CAPTURE_PATH = os.path.join('temp','capture','temp.pcap')
local_capture_file = os.path.join('temp','capture','capture.pcap')

def root():
    #进行root
    root_cmd = ['adb', 'root']
    result = subprocess.run(root_cmd, capture_output=True, text=True)
    #print(result.stdout)
    sleep(10)#等root
    print('root finish')

def start_tcpdump(temp_file):
    capture_cmd = ['adb', 'shell', f'tcpdump -i any -p -s 0 -w {temp_file} not host 172.16.1.2']
    proc = subprocess.Popen(capture_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc

def stop_tcpdump(proc):
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()

def pull_file(remote_file, local_file):
    pull_cmd = ['adb', 'pull', remote_file, local_file]
    result = subprocess.run(pull_cmd, capture_output=True, text=True)

def merge_files(src_file, dest_file):
    writer = PcapWriter(dest_file, append=True)
    reader = PcapReader(src_file)
    for pkt in reader:
        writer.write(pkt)
    reader.close()
    writer.close()

def check_and_clear_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    open(file_path, 'w').close()



def get_protocol_name(packet):
    layers = []
    current_layer = packet
    while current_layer:
        layers.append(current_layer.name)
        current_layer = current_layer.payload

    # 去除'cooked linux'协议，找到最后一个非'cooked linux'的协议名
    protocol_name = None
    for layer in reversed(layers):
        if layer != 'cooked linux':
            protocol_name = layer
            break

    if protocol_name:
        return protocol_name
    else:
        return 'Unknow'


def convert_to_csv(pcap_file, csv_file):
    with PcapReader(pcap_file) as packets, open(csv_file, 'w', newline='') as out_csv:
        csv_writer = csv.writer(out_csv)
        csv_writer.writerow(['timestamp', 'src', 'dst','protocol', 'protocol_name', 'length'])

        for packet in packets:
            src = packet[IP].src if IP in packet else ''
            dst = packet[IP].dst if IP in packet else ''
            protocol = packet[IP].proto if IP in packet else ''
            protocol_name = get_protocol_name(packet)
            length = len(packet)

            # 写入每个数据包的信息
            csv_writer.writerow([packet.time, src, dst,protocol, protocol_name, length])

def csv_to_dataframe(csv_file):
    # 读取CSV文件到DataFrame
    df = pd.read_csv(csv_file)
    return df


class PacketCapture(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.data = None
        check_and_clear_file(local_capture_file)
        root()

    def run(self):
        while not self._stop_event.is_set():
            temp_file = '/sdcard/temp.pcap'
            proc = start_tcpdump(temp_file)
            time.sleep(10)  # 等待一段时间以收集足够的数据包
            stop_tcpdump(proc)

            local_temp_file = TEMP_CAPTURE_PATH
            check_and_clear_file(local_temp_file)
            pull_file(temp_file, local_temp_file)
            merge_files(local_temp_file, local_capture_file)

            # 使用函数转换文件
            convert_to_csv(CAPTURE_PATH, CSV_PATH)
            file_path = CSV_PATH

            if os.path.exists(file_path):
                self.data = csv_to_dataframe(CSV_PATH)
                #print(self.data)

    def stop(self):
        self._stop_event.set()

    def get_data(self):
        return pd.DataFrame(self.data)

#tcpdump -i any -p -s 0 -w /sdcard/temp.pcap -v -nn not host 172.16.1.2
