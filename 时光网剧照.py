#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import json
import os
import sys
import time
import traceback
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
import urllib3
from requests.adapters import HTTPAdapter

urllib3.disable_warnings()

movie_id = 'YOUR MOVIEID'


def get_image_json():
    url = 'http://movie.mtime.com/' + movie_id + '/posters_and_images/'
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
    soup = BeautifulSoup(result, "html.parser")
    script_list = soup.find_all('script')
    for each in script_list:
        if each.get_text().find('imageList') > 0:
            image_list_list_str = each.get_text().split('=')[1]
            break
    image_list_list = json.loads(image_list_list_str)
    return image_list_list


def get_image_id(image_list):
    officialstageimage = image_list[0]['stagepicture'][0]['officialstageimage']
    screenshotstageimage = image_list[0]['stagepicture'][1]['screenshotstageimage']
    otherstageimage = image_list[0]['stagepicture'][2]['otherstageimage']
    generalposter = image_list[1]['poster'][0]['generalposter']
    forecastposter = image_list[1]['poster'][1]['forecastposter']
    roleposter = image_list[1]['poster'][2]['roleposter']
    otherposter = image_list[1]['poster'][3]['otherposter']
    officialworkimage = image_list[2]['workimage'][0]['officialworkimage']
    makeupworkimage = image_list[2]['workimage'][1]['makeupworkimage']
    conceptworkimage = image_list[2]['workimage'][2]['conceptworkimage']
    studioworkimage = image_list[2]['workimage'][3]['studioworkimage']
    image_array_list = (
    officialstageimage, screenshotstageimage, otherstageimage, generalposter, forecastposter, roleposter, otherposter,
    officialworkimage, makeupworkimage, conceptworkimage, studioworkimage)

    each_type_list = []
    for each_image_array in image_array_list:
        if len(each_image_array):
            key = each_image_array[0]['title'].split(' ')[0]
            id_list = []
            each_type_dic = {}
            for each_image in each_image_array:
                # title = each_image['title']
                id = each_image['id']
                id_list.append(id)
            each_type_dic[key] = id_list
            each_type_list.append(each_type_dic)

    print(each_type_list)
    return each_type_list


def get_image(id_list):
    for each_id_list in id_list:
        name = list(each_id_list.keys())[0]
        each_type_id_list = each_id_list[name]
        print("开始下载{} 共{}张".format(name, len(each_type_id_list)))
        for each_id in each_type_id_list:
            download_image(name, str(each_id))


def download_image(name, id):
    base_url = 'http://service.library.mtime.com/Comment.api?'
    header = {
        'Cookie': '_tt_=2177CD3A094773EA08072B5636CFA4CC; _userCode_=20202282223178194; _userIdentity_=20202282223178408; DefaultCity-CookieKey=879; DefaultDistrict-CookieKey=0; Hm_lvt_6dd1e3b818c756974fb222f0eae5512e=1582899799,1582900402; __utma=196937584.231409643.1582900402.1582900402.1582900402.1; __utmc=196937584; __utmz=196937584.1582900402.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; maxShowNewbie=2; searchHistoryCookie=%u4E07%u7BAD%u7A7F%u5FC3; _ydclearance=7445c1b25ad10064f045d068-894f-4989-a084-fc7f5c57f599-1582907611; _movies_=180795; _oss_=1; _ati_=PrsUMMHnr45Uk96kTENgKgyI2k%2B049u3B5uaqrk0nYDAiwcj818t429%2BcSZKGqVTOFX60WyDPgs0dUEWUqX5Z3zZOaWKmGKxEipB4r9S6569CdSWbMqGWcUAwOFsosmNRTy84kMhAPx9eUwMpZ0%2FJUSASR7voT2K4ohtAPN7grAnfodgQ8emvFMJ259hhGHSc5j54XlsW2GpAf3NKO8%2BIjX9aMKlkTaBhT%2BvhYvUdguJ2iTD3TEM%2BAGJJOsNM07uzUUHAMu2eSz0nQ%2By3tNZWPb9%2FBSvneEqnRif8YocFuwHLUZZcEwByzhQND0MoqP3IycIo7fYxzpYV9AZtIYT8sIHFss9Zky7%2FBmCP01EBIc%2F0SCUTC1YXQJtjZxhUJd4FetJDBKWoU8HXwiIYy2yRgdpYZQrccmkcIowNNbhfHCteOCNfgH7bQ96xlzOhcEpNw9BXg8oWMV4me9UH9ncJg%3D%3D; loginEmail=18227590678; _mi_=162729c224cef554ad234148c14e2bbc; _mu_=07A23FFF9EC6E421851DD729464DE203; Hm_lpvt_6dd1e3b818c756974fb222f0eae5512e=1582902187',
        'Host': 'service.library.mtime.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
    }
    timeStamp = int(round(time.time() * 1000))
    now = '2020228' + datetime.datetime.now().strftime('%H%M%S%f')[:-1]

    param = {
        'Ajax_CallBack': 'true',
        'Ajax_CallBackType': 'Mtime.Library.Services',
        'Ajax_CallBackMethod': 'DownloadNoWatermarkImage',
        'Ajax_CrossDomain': 1,
        'Ajax_RequestUrl': 'http://movie.mtime.com/' + movie_id + '/posters_and_images/' + id + '/',
        't': now,
        'Ajax_CallBackArgument0': id
    }
    url = base_url + urlencode(param)
    try:
        response = requests.get(url, headers=header, verify=False, timeout=(3, 10))  # 传参并发起请求
    except:
        print('获取失败 id：{}'.format(id))
        return

    result = response.text
    result_split = result.split('=')[1:]
    a = ''
    for each in result_split:
        a = a + '=' + each
    result_str = a[1:].split(';')[0]
    result_json_url = json.loads(result_str)['value']['src']
    handle_download(name, result_json_url)


def handle_download(name, url):
    file_dir = r"\mtime"
    is_dir_exists = os.path.exists(file_dir)
    if not is_dir_exists:
        os.makedirs(file_dir)
    try:
        s = requests.Session()
        s.mount(url, HTTPAdapter(max_retries=5))
        downloaded = s.get(url, timeout=(5, 10))
        file_name = name + "_1.jpg"
        file_path = file_dir + os.sep + file_name
        for i in range(1, 100):
            if os.path.isfile(file_path):
                name_multi = name + '_' + str(i)
                file_name = name_multi + ".jpg"
                file_path = file_dir + os.sep + file_name
            else:
                break
        print(file_name)
        with open(file_path, 'wb') as f:
            f.write(downloaded.content)
    except Exception as e:
        print('下载失败: ', e)
        traceback.print_exc()


if __name__ == '__main__':
    image_list = get_image_json()
    id_list = get_image_id(image_list)
    get_image(id_list)
