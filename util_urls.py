import requests
import base64
def get_url_id(url):
    url_bytes = url.encode("utf-8")
    url_id = base64.urlsafe_b64encode(url_bytes).decode().strip("=")
    return url_id

def check_url_with_api(url):
    headers = {
        "x-apikey": "c0d7ffa4bb65e8b388580fed496e8ae443edb8ebab4e551fe348e9442faa3ce4"
    }
    url_id = get_url_id(url)

    url_report_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    response = requests.get(url_report_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None
