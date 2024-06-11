import cv2
from pyzbar.pyzbar import decode
import os
# import threading
import requests
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np
import streamlit as st

curdir = os.getcwd()  # 获取当前路径current work directory

data_dir = os.path.join(curdir, r"temp\data")


# 创建文件夹
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def check_for_apk(directory=data_dir):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.apk'):
                return 1
    return -1


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


def get_qrcode(image_binary):
    nparr = np.frombuffer(image_binary, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    decoded_objects = decode(img)
    for obj in decoded_objects:
        if obj.type == 'QRCODE':
            return obj.data.decode('GBK')
    return None


def generate_header():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
        'Date': current_time,
    }
    return header


def download_single_apk(apk_url, progress_callback=None):
    save_path = os.path.join(data_dir, os.path.basename(apk_url))
    try:
        with requests.get(apk_url, headers=generate_header(), allow_redirects=True, timeout=180, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            chunk_size = 1024
            downloaded_size = 0

            with open(save_path, "wb") as hf:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        hf.write(chunk)
                        downloaded_size += len(chunk)
                        progress = downloaded_size / total_size * 100
                        st.session_state['progress'] = progress/100
                        if progress_callback:
                            progress_callback()
                        print(f"\r正在下载中: {progress:.2f}%", end="")

        print("\n下载完成！")
        return 0
    except Exception as e:
        print("发生错误,无法下载APK")
        print(e)
        return -1


    except Exception as e:
        print("发生错误,无法下载APK")
        print(e)
        return -1


def download_apk(method_code=1, url = None, qrcode = None, progress_callback=None):
    if method_code == 1:
        if is_apk_url(url):
            download_single_apk(url, progress_callback)
        else:
            return -1
    elif method_code == 2:
        urls = get_qrcode(qrcode)
        if is_apk_url(urls):
            download_single_apk(urls,progress_callback)
        else:
            urls_a = get_all_links(urls)
            for apk_url in urls_a:
                download_single_apk(apk_url,progress_callback)
    elif method_code == 3:
        urls_a = get_all_links(url)

        for apk_url in urls_a:
            download_single_apk(apk_url,progress_callback)
    else:
        pass
    return check_for_apk()
