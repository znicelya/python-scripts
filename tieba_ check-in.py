import json

import requests

user_info_url = 'https://tieba.baidu.com/f/user/json_userinfo?_=1679566186572'
concern_url = 'https://tieba.baidu.com/mg/o/getForumHome?st=0&pn=1\
&rn=20&eqid=98e53f090000f30300000006641c21ac&refer=www.baidu.com'

# 这里填入cookie，可填入多个
cookies = [
    '',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)\
     AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Cookie': ''
}

for cookie in cookies:
    headers['Cookie'] = cookie
    res = requests.get(user_info_url, headers=headers)
    login_res = json.loads(res.text)
    if login_res['no'] == 0:
        if login_res['data']['is_login'] == 1:
            print('🥰登录成功，开始获取关注列表...')
            print(f"用户 {login_res['data']['user_name_weak']} 开始签到...")
            concern_res = requests.get(concern_url, headers=headers).text
            for item in json.loads(concern_res)['data']['like_forum']['list']:
                print(f'开始签到👉 {item["forum_name"]} 👈吧...')
                check_in_url = f'https://tieba.baidu.com/sign/add'
                check_res = requests.post(check_in_url, headers=headers, data={
                    'ie': 'utf-8',
                    'kw': item['forum_name'],
                    'tbs': '3453bf23577bea101679566311'
                }).text
                print(json.loads(check_res))
    else:
        print('登录失败')
