from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器窗口
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 自动下载和安装Chrome驱动
service = Service(ChromeDriverManager().install())

# 创建浏览器驱动
driver = webdriver.Chrome(service=service, options=chrome_options)

# 已访问链接集合，避免重复访问
visited_links = set()


def fetch_links(url):
    if url in visited_links:
        return []

    visited_links.add(url)
    driver.get(url)

    # 等待页面加载完成
    time.sleep(5)  # 根据需要调整等待时间

    # 滚动到页面底部以加载所有内容
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # 根据需要调整等待时间

    # 获取所有链接
    links = driver.find_elements(By.TAG_NAME, 'a')
    extracted_links = [link.get_attribute('href') for link in links if link.get_attribute('href')]

    nested_links = []
    for link in extracted_links:
        if 'im.qq.com' in link and link not in visited_links:
            nested_links.extend(fetch_links(link))

    return extracted_links + nested_links


# 目标URL
url = 'https://im.qq.com/index/#downloadAnchor'
all_links = fetch_links(url)

# 输出所有链接
for link in all_links:
    print(link)

# 关闭浏览器
driver.quit()





# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# import time
#
# visited = set()
#
# def get_links_from_html(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     links = set()
#     for a_tag in soup.find_all('a', href=True):
#         links.add(a_tag['href'])
#     return links
#
# def crawl(url, depth=3):
#     if depth == 0 or url in visited:
#         return
#     visited.add(url)
#     print(f'Crawling: {url}')
#
#     # Handle static content
#     response = requests.get(url)
#     if response.status_code != 200:
#         return
#     links = get_links_from_html(response.text)
#     print(f'Found {len(links)} links on {url}')
#
#     # Handle dynamic content
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # Update this path
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#
#     try:
#         driver.get(url)
#         WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
#         time.sleep(5)  # Wait for dynamic content to load, adjust as necessary
#         dynamic_html = driver.page_source
#         dynamic_links = get_links_from_html(dynamic_html)
#         links.update(dynamic_links)
#         print(f'Found {len(dynamic_links)} dynamic links on {url}')
#     except Exception as e:
#         print(f'Error crawling {url}: {e}')
#     finally:
#         driver.quit()
#
#     for link in links:
#         if link.startswith('http'):  # Basic check to ensure we only follow valid URLs
#             crawl(link, depth - 1)
#
# if __name__ == "__main__":
#     start_url = 'https://im.qq.com'  # Replace with your starting URL
#     crawl(start_url)
