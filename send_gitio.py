import requests
import datetime
import re
import os
from openpyxl.styles.builtins import title

import config.connect
from config import *

connect_config = config.connect.Insert_sql(redis_db='github_io', mysql_db='github_io')

today = datetime.datetime.now().strftime('%Y-%m-%d')


def get_text():
    pageIndex = 0
    while (connect_config.redis_llen('git_url')):
        pageIndex += 1
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/136.0.0.0',
        }

        params = {
            'article_type_id': '3',
            'platform_id': '99',
            'pageIndex': pageIndex
        }

        res = requests.get(
            'https://lifewillfindaway.top/api/website/getNews',
            params=params,
            headers=headers,
            # verify=False,
        )
        res_json = res.json()
        for data in res_json['data']['data']:
            if not connect_config.redis_llen('git_url'):
                break
            title = data['title']
            title = re.sub(r'[<>:"/\\|?*]', '', title)
            content = data['content']
            send_md(title, content)


def send_md(title, content):
    send_path('_posts')
    file_name = f'_posts/{today}-{title}.md'
    with open(file_name, 'w', encoding='utf-8') as f:
        first_paragraphs = """---
layout: post
post title: "{}" 
description: "{}" 
date: {}
---""".format(title, title, today)
        links = ''
        range_num = connect_config.redis_llen('git_url')
        if range_num >= 5:
            range_num = 5
        for i in range(range_num):
            url = 'https://' + connect_config.redis_pop('git_url').replace('"', '')
            links += f'\n\n{url}'

        f.write(f'{first_paragraphs}\n\n{content}{links}')

    return


def send_path(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return


if __name__ == "__main__":
    get_text()
    print('success')
