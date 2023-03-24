import time

import requests
from bs4 import BeautifulSoup


class Proxy:
    def __init__(self):
        self.proxies_list = []
        self.can_use = []
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'

    def send_request(self, page):
        base_url = f'https://www.kuaidaili.com/free/inha/{page}'
        headers = {
            'User-Agent': self.ua
        }
        # 发送请求：模拟浏览器发送请求，获取响应数据
        response = requests.get(base_url, headers=headers)
        data = response.content.decode()
        time.sleep(1)
        return data

    def parse_dom(self, content):
        # 使用BeautifulSoup解析页面
        soup = BeautifulSoup(content, 'html.parser')
        trs = soup.find_all('tr')
        # print(trs)
        for tr in trs:
            proxies_dict = {}
            dip = tr.find('td', attrs={'data-title': 'IP'})
            dport = tr.find('td', attrs={'data-title': 'PORT'})
            dtype = tr.find('td', attrs={'data-title': '类型'})
            if dip is not None and dport is not None and dtype is not None:
                print(dtype.text.strip(), dip.text.strip(), dport.text.strip())
                proxies_dict[dtype.text.strip()] = dip.text.strip() + ":" + dport.text.strip()
                self.proxies_list.append(proxies_dict)

    def check_ip(self, proxies_list):
        headers = {
            'User-Agent': self.ua
        }
        can_use = []
        for proxies in proxies_list:
            try:
                response = requests.get('https://www.baidu.com/', headers=headers, proxies=proxies, timeout=0.1)
                if response.status_code == 200:
                    can_use.append(proxies)
            except Exception as e:
                print(e)

        return can_use

    def save_proxy(self):
        with open('./IP.txt', 'w') as file:
            for i in range(len(self.can_use)):
                s = str(self.can_use[i]) + '\n'
                file.write(s)

    def run(self):
        for page in range(1, 100):
            data = self.send_request(page)
            self.parse_dom(data)
        print("获取到的代理IP数量：", len(self.proxies_list))
        # 检查代理是否可用
        self.can_use = self.check_ip(self.proxies_list)
        print("能用的代理IP数量：", len(self.can_use))
        self.save_proxy()


if __name__ == '__main__':
    proxy = Proxy()
    proxy.run()
