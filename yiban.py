import json
import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

tags_url = 'https://yiban.io/style_center/0_0_0'
response = requests.get(tags_url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
ul = soup.find('ul', class_='style-tag-list')
outlis = ul.find_all('li', class_='style-tag-li clearfix')
wc_list = []
for outli in outlis:
    pp = outli.find('a').text.strip()
    if pp != '模板':
        count_url = f'https://yiban.io/api/article_editor/material/list/new?tag_id=0&page=1&length=60&order_rule=hot_rank&tag_title={pp}'
        for i in range(json.loads(requests.get(count_url, headers=headers).text)['total_page']):
            print(i + 1)
            page_url = f'https://yiban.io/api/article_editor/material/list/new?tag_id=0&page={i + 1}&length=60&order_rule=hot_rank&tag_title={pp}'
            res = json.loads(requests.get(page_url, headers=headers).text)['materials']
            for item in res:
                tags = item['tags']
                del item['tags']
                del item['tags_id']
                if len(tags) > 0:
                    item['tags'] = ','.join(tuple([tag for tag in tags if tag is not None]))
                wc_list.append(item)
    else:
        for i in range(6):
            page_url = f'https://yiban.io/api/style_center/template/list?offset={i * 100}&limit=100&keyword=&order_rule=hot_rank&tag_title='
            style_template_list = json.loads(requests.get(page_url, headers=headers).text)['style_template_list']
            for template in tqdm(style_template_list):
                created_at = template['created_at']
                _id = template['id']
                date = time.strftime('%Y%m%d', time.localtime(float(created_at)))
                detail_url = f'https://yiban.io/style_detail/template/{date}/{_id}.html'
                # print(detail_url)

                # 1. explorer settings
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                for k, v in headers.items():
                    options.add_argument(f'{k}={v}')

                # 2. browser driver
                browser = webdriver.Chrome(chrome_options=options)
                browser.get(detail_url)

                detail_soup = BeautifulSoup(browser.page_source, 'html.parser')
                detail = detail_soup.find('div', class_='template-box').find('section')
                item = {
                    'category': '1',
                    'create_at': template['created_at'],
                    'deleted': template['deleted'],
                    'desc': '',
                    'detail': str(detail),
                    'display_name': template['display_name'],
                    'fav_count': template['fav_count'],
                    'faved': template['faved'],
                    'free': template['free'],
                    'is_top': 0,
                    'paid_count': template['paid_count'],
                    'second_category': '1',
                    'star': True,
                    'star_at': '',
                    'tags': ','.join([template['tags'][tag] for tag in template['tags']]),
                    'use_count': template['use_count'],
                    'update_at': template['updated_at']
                }
                print(json.dumps(item, ensure_ascii=False))
                wc_list.append(item)

with open('./wc.json', 'w', encoding='utf8') as wc:
    wc.write(json.dumps(wc_list, ensure_ascii=False))
