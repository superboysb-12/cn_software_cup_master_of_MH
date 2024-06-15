import os
import subprocess
from scapy.all import PcapReader, PcapWriter, IP
from time import sleep
import csv
import pandas as pd

def start_tcpdump(temp_file):
    capture_cmd = ['adb', 'shell', f'tcpdump -i any -w {temp_file}']
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
    print(result.stdout)


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
    # 打印DataFrame
    print(df)


# 假设 'temp' 目录位于项目根目录下
local_capture_file = 'temp/capture.pcap'
check_and_clear_file(local_capture_file)

times = 0
while True:
    print(times)
    times+=1
    temp_file = '/sdcard/temp.pcap'
    proc = start_tcpdump(temp_file)
    sleep(10)  # 等待一段时间以收集足够的数据包

    stop_tcpdump(proc)

    local_temp_file = 'temp/temp.pcap'
    check_and_clear_file(local_temp_file)

    pull_file(temp_file, local_temp_file)

    merge_files(local_temp_file, local_capture_file)
    # 使用函数转换文件
    convert_to_csv('temp/capture.pcap', 'temp/capture.csv')
    csv_to_dataframe('temp/capture.csv')

