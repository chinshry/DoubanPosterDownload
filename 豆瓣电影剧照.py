#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import traceback
import requests
import urllib3
from lxml import etree

urllib3.disable_warnings()

movie_id = 'YOUR MOVIEID'
start = 0

def get_url():
    # 官方剧照 o
    still_url = 'https://movie.douban.com/subject/'+movie_id+'/photos?type=S&sortby=like&size=a&subtype=o'
    # 工作照 w
    work_url = 'https://movie.douban.com/subject/'+movie_id+'/photos?type=S&sortby=like&size=a&subtype=w'
    # 正式海报
    official_poster_url = 'https://movie.douban.com/subject/'+movie_id+'/photos?type=R&sortby=like&size=a&subtype=o'
    # 预告海报
    preview_poster_url = 'https://movie.douban.com/subject/'+movie_id+'/photos?type=R&sortby=like&size=a&subtype=p'
    # 角色海报
    role_poster_url = 'https://movie.douban.com/subject/'+movie_id+'/photos?type=R&sortby=like&size=a&subtype=r'
    # 其他海报
    other_poster_url = 'https://movie.douban.com/subject/'+movie_id+'/photos?type=R&sortby=like&size=a&subtype=t'
    return (('官方剧照',still_url), ('工作照', work_url), ('正式海报',official_poster_url), ('预告海报', preview_poster_url), ('角色海报',role_poster_url), ('其他海报',other_poster_url))


def download_img(name, img_id):
    url1 = 'https://img1.doubanio.com/view/photo/raw/public/p' + img_id + '.jpg'
    file_dir = r"db_download"
    is_dir_exists = os.path.exists(file_dir)
    if not is_dir_exists:
        os.makedirs(file_dir)
    header = {
        'Referer': 'https://movie.douban.com/photos/photo/' + img_id + '/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
    }
    try:
        downloaded = requests.get(url1, headers=header, stream=True)
    except Exception as e:
        print('下载失败: ', e)
        downloaded = None
        traceback.print_exc()
    if downloaded is not None:
        file_name = name + "_1.jpg"
        file_path = file_dir + os.sep + file_name
        for i in range(1, 1000):
            if os.path.isfile(file_path):
                name_multi = name + '_' + str(i)
                file_name = name_multi + ".jpg"
                file_path = file_dir + os.sep + file_name
            else:
                break
        print(file_name)
        with open(file_path, 'wb') as f:
            f.write(downloaded.content)




def get_img_id_list(url_info):
    pages, img_id = get_page(url_info[1])
    if pages != 1:
        for page in range(1, pages):
            _, img_id_add = get_page(url_info[1], str(page*30))
            img_id += img_id_add
    print(img_id)
    print("开始下载{} 共{}张".format(url_info[0], len(img_id)))

    for each_img_id in img_id:
        download_img(url_info[0], each_img_id)

def get_page(url, start = '0'):
    final_url = url + '&start=' + start
    header = {
        'Host': 'movie.douban.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
    }
    try:
        response = requests.get(final_url, headers=header, verify=False, timeout=(3, 10))  # 传参并发起请求
    except Exception as e:
        print(e)
        return
    result = response.text
    pages, img_id = sync_page(result)
    return pages, img_id

def sync_page(result):
    content = etree.HTML(result)
    page_num = content.xpath('//span[@class="count"]/text()')
    if len(page_num):
        pages = int(page_num[0][:-2].split('共')[1])//30+1
    else:
        pages = 1
    img_id = content.xpath('//ul[@class="poster-col3 clearfix"]/li/@data-id')
    return pages, img_id


if __name__ == '__main__':
    page_url_list = get_url()
    for each in page_url_list:
        get_img_id_list(each)
