import os
import subprocess
from scapy.all import PcapReader, PcapWriter, IP
from time import sleep
import csv
import pandas as pd
import threading
import time
import os


def root():
    #进行root
    root_cmd = ['adb', 'root']
    result = subprocess.run(root_cmd, capture_output=True, text=True)
    print(result.stdout)
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
    #print(result.stdout)

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

def convert_to_csv(pcap_file, csv_file):
    with PcapReader(pcap_file) as packets, open(csv_file, 'w', newline='') as out_csv:
        csv_writer = csv.writer(out_csv)
        # 写入标题行，这里只是一个示例，您可能需要根据实际情况添加或删除字段
        csv_writer.writerow(['timestamp', 'src', 'dst', 'protocol', 'length'])

        for packet in packets:
            # 提取数据包信息，这里只是一个示例，您可能需要根据实际情况添加或删除字段
            src = packet[IP].src if IP in packet else ''
            dst = packet[IP].dst if IP in packet else ''
            protocol = packet[IP].proto if IP in packet else ''
            length = len(packet)

            # 写入每个数据包的信息
            csv_writer.writerow([packet.time, src, dst, protocol, length])

def csv_to_dataframe(csv_file):
    # 读取CSV文件到DataFrame
    df = pd.read_csv(csv_file)
    return df

# 假设 'temp' 目录位于项目根目录下
local_capture_file = 'temp/capture.pcap'
check_and_clear_file(local_capture_file)

'''
thread = None
thread_lock = threading.Lock()  # 添加一个锁对象
def run_capture(stdf,df_call_back):

    root()
    times = 0
    while True:
        #print(times)
        times += 1
        temp_file = '/sdcard/temp.pcap'
        proc = start_tcpdump(temp_file)
        time.sleep(10)  # 等待一段时间以收集足够的数据包
        stop_tcpdump(proc)

        local_temp_file = 'temp/temp.pcap'
        check_and_clear_file(local_temp_file)
        pull_file(temp_file, local_temp_file)
        merge_files(local_temp_file, local_capture_file)

        # 使用函数转换文件
        convert_to_csv('temp/capture.pcap', 'temp/capture.csv')
        file_path = 'temp/capture.csv'

        if os.path.exists(file_path):
            stdf = csv_to_dataframe('temp/capture.csv')
            with thread_lock:  # 使用锁保护共享资源
                df_call_back(stdf)

def start_capture(stdf,df_call_back):
    global thread
    thread = threading.Thread(target=run_capture,args=(stdf,df_call_back))
    thread.start()
    print('capture start')

def stop_capture():
    global thread
    thread.join()
'''


class PacketCapture(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.data = None
        root()

    def run(self):
        while not self._stop_event.is_set():
            temp_file = '/sdcard/temp.pcap'
            proc = start_tcpdump(temp_file)
            time.sleep(10)  # 等待一段时间以收集足够的数据包
            stop_tcpdump(proc)

            local_temp_file = 'temp/temp.pcap'
            check_and_clear_file(local_temp_file)
            pull_file(temp_file, local_temp_file)
            merge_files(local_temp_file, local_capture_file)

            # 使用函数转换文件
            convert_to_csv('temp/capture.pcap', 'temp/capture.csv')
            file_path = 'temp/capture.csv'

            if os.path.exists(file_path):
                self.data = csv_to_dataframe('temp/capture.csv')
                print(self.data)


    def stop(self):
        self._stop_event.set()

    def get_data(self):
        return pd.DataFrame(self.data)
#root()
#capture()
#tcpdump -i any -p -s 0 -w /sdcard/temp.pcap not host 172.16.1.2
#tcpdump -i any -p -s 0 -w /sdcard/temp.pcap -v -nn
#tcpdump -i any -p -s 0 -w /sdcard/temp.pcap -vvv -nn