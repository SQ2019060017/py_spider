import os
import requests
from pyquery import PyQuery as pq
import secret


def get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.110 '
                      'Safari/537.36',
        'Cookie': secret.cookie,

    }
    r = requests.get(url, headers=headers)
    print('status_code', r.status_code)
    page = r.content
    return page


def main():
    url = 'https://www.zhihu.com/follow'
    page = get(url)
    print(page.decode())


if __name__ == '__main__':
    main()
