import cv2
from pyzbar.pyzbar import decode
import os
import threading
import requests
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

curdir = os.getcwd()  # 获取当前路径current work directory

data_dir = os.path.join(curdir, "data")

# 创建文件夹
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def check_for_apk(directory=data_dir):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.apk'):
                return True
    return False


def get_redirected_url(url, page_url):
    try:
        if not url.startswith('http'):
            url = page_url + url  # 拼接成绝对URL
        response = requests.head(url, allow_redirects=True)
        redirected_url = response.url
        return redirected_url
    except requests.RequestException as e:
        print("Error:", e)
        return None


def get_static_links(url):
    # 发送GET请求获取页面内容
    response = requests.get(url)
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # 找到所有的<a>标签
    links = soup.find_all('a')
    # 提取链接
    all_links = [link.get('href') for link in links if link.get('href')]

    return all_links


def get_dynamic_links(url):
    # 使用Selenium模拟浏览器行为
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # 无头模式
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # 提取动态加载后的链接
    dynamic_links = driver.execute_script(
        'return [].map.call(document.querySelectorAll("a"), function(link) { return link.href; })')

    driver.quit()

    return dynamic_links


def get_all_links(url):
    static_links = get_static_links(url)
    dynamic_links = get_dynamic_links(url)
    all_links = static_links + dynamic_links  # 将动态链接添加到列表中
    apk_links = []
    for link in all_links:
        if is_apk_url(link):
            apk_links.append(link)
        else:
            redirected_url = get_redirected_url(link, url)  # 传递page_url参数
            if redirected_url and is_apk_url(redirected_url):
                apk_links.append(redirected_url)

    return apk_links


def is_apk_url(url):
    return url.endswith('.apk')


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
        'Date': current_time,
    }
    return header


def download_single_apk(apk_url):
    # print(apk_url)
    save_path = os.path.join(curdir, "data", "%s" % os.path.basename(apk_url))
    try:
        r = requests.get(apk_url, headers=generate_header(), allow_redirects=True, timeout=180)  # 发起requests下载请求
        status_code = r.status_code
        if (status_code == 200 or status_code == 206):
            with open(save_path, "wb") as hf:
                hf.write(r.content)
        print("正在下载中！")
        return 0

    except:
        print("发生错误,无法下载APK")
        return -1


def download_apk(method_code, url = None, qrcode = None):
    if method_code == 1:
        download_single_apk(url)
    elif method_code == 2:
        urls = get_qrcode(qrcode)
        for url_a in urls:
            if is_apk_url(url_a):
                download_single_apk(url_a)
            else:
                urls_a = get_all_links(url_a)
                for apk_url in urls_a:
                    download_single_apk(apk_url)
    elif method_code == 3:
        urls_a = get_all_links(url)

        for apk_url in urls_a:
            download_single_apk(apk_url)
    else:
        pass
    return check_for_apk()

###批量下载的线程
# class DownLoadThread(threading.Thread):
#     def __init__(self, q_job):
#         self._q_job = q_job
#         threading.Thread.__init__(self)
#
#     def run(self):
#         while True:
#             if self._q_job.qsize() > 0:
#                 download_single_apk(self._q_job.get())  # 这是10个线程都运行这个下载函数
#             else:
#                 break


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
