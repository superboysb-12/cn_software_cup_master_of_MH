import cv2
from pyzbar.pyzbar import decode
import os
import threading
import requests
import datetime

def get_qrcode(image_path):
    img = cv2.imread(image_path)
    decoded_objects = decode(img)
    for obj in decoded_objects:
        if obj.type == 'QRCODE':
            return obj.data.decode('utf-8')

def generate_header():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
        'Date': current_time,  # 可选项，如果你需要在 header 中包含当前时间
        # 其他自定义 header 字段
    }
    return header


curdir = os.getcwd()  # 获取当前路径current work directory

# 创建文件夹
if not os.path.exists("downloaded_apk"):
    os.system("mkdir downloaded_apk")


def download_single_apk(apk_url):
    '''下载单个apk文件'''
    # print(apk_url)
    current_time = datetime.datetime.now()
    current_time = current_time.strftime('%Y-%m-%d_%H_%M_%S')
    save_path = os.path.join(curdir, "downloaded_apk", "%s.apk" % current_time)
    if not os.path.exists(save_path):  # 避免二次下载
        print("Downloading  %s" % (save_path))
        try:
            r = requests.get(apk_url, headers=generate_header(), allow_redirects=True, timeout=720)  # 发起requests下载请求
            status_code = r.status_code
            if (status_code == 200 or status_code == 206):
                with open(save_path, "wb") as hf:
                    hf.write(r.content)
        except:
            print("Error, can not download apk" )
    else:
        print("%s downloaded already!" % save_path)


###批量下载的线程
class DownLoadThread(threading.Thread):
    def __init__(self, q_job):
        self._q_job = q_job
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self._q_job.qsize() > 0:
                download_single_apk(self._q_job.get())  # 这是10个线程都运行这个下载函数
            else:
                break


# if __name__ == '__main__':
#     # 初始化一个队列
#     q = queue.Queue(0)
#
#     # 逐行读取excel里的url
#     excel = openpyxl.load_workbook('Top_1000_app.xlsx')  # 读取excel里边的内容
#     table = excel.active
#     rows = table.max_row
#     for r in range(2, rows + 1):  # 跟excel的第一行标题行无关，从第二行文字内容开始做替换工作
#         apk_name = table.cell(row=r, column=2).value  # 获取app名字（中文）
#         apk_url = table.cell(row=r, column=3).value  # 获取下载地址
#         temp_str = apk_name + ";" + apk_url  # 不可以put列表进队列，只能尝试put字符串
#         q.put(temp_str)
#
#     for i in range(10):  # 开启10个线程
#         DownLoadThread(q).start()
