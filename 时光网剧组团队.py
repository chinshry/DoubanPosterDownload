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
        'Cookie': '_tt_=2177CD3A094773EA08072B5636CFA4CC; maxShowNewbie=2; loginEmail=18227590678; _isNewbie_=isNewBie; DefaultCity-CookieKey=290; __utma=196937584.231409643.1582900402.1584261326.1586185637.3; __utmz=196937584.1586185637.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; searchHistoryCookie=%u604B%u66F21980%2C%u62B5%u8FBE%u4E4B%u8C1C%2C%u521D%u604B%u672A%u6EE1%2C%u73A9%u547D%u8BD5%u7231%2C%u6BCD%u94C1%u519B; __utmz=221034756.1586611205.40.7.utmcsr=people.mtime.com|utmccn=(referral)|utmcmd=referral|utmcct=/1979927/filmographies/; _ydclearance=750aab053dd98376c99f1457-bff5-4014-bc3b-36a8ecad3bd3-1589039217; _userCode_=20205921477386; _userIdentity_=202059214773301; _movies_=266571.254336.230647.264766; __utma=221034756.1874126222.1582900413.1586611205.1589032038.41; __utmc=221034756; __utmt=1; __utmt_~1=1; Hm_lvt_6dd1e3b818c756974fb222f0eae5512e=1589032038; __utmb=221034756.4.10.1589032038; Hm_lpvt_6dd1e3b818c756974fb222f0eae5512e=1589032094',
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
