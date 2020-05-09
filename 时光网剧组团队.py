#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
import urllib3
from lxml import etree
urllib3.disable_warnings()

movie_id = 'YOUR MOVIEID'


def get_image_json():
    url = 'http://movie.mtime.com/' + movie_id + '/fullcredits.html'
    header = {
        'Cookie': 'YOUR Cookie',
        'Host': 'movie.mtime.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=header, verify=False, timeout=(3, 10))  # 传参并发起请求
    except Exception as e:
        print(e)
        return

    result = response.text
    content = etree.HTML(result)
    title = content.xpath('//div[@class="clearfix"]/h1//text()')
    print(title[0])
    credits_list = content.xpath('//div[@class="credits_list"]//text()')

    for each in credits_list:
        print(each)

if __name__ == '__main__':
    get_image_json()
