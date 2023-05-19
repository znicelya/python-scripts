import requests
from urllib.parse import urlencode

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
     (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
    'cookie': '此处填入cookie',
}

speak = [
    '青虫娘,求上传',
    '青虫娘,求下载',
    '青虫娘,求魔力',
    '青虫娘,v我50',
]

for s in speak:
    params = {
        'shout': '我喊',
        'sent': 'yes',
        'type': 'shoutbox',
        'shbox_text': s
    }
    result = urlencode(params)
    every = f'https://cyanbug.net/shoutbox.php?{result}'
    response = requests.get(every, headers=headers)
