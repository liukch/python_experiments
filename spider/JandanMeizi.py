#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver

urls = ('http://jandan.net/ooxx/page-{}#comments'.format(i) for i in range(300, 327))
x = 1

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'

driver = webdriver.PhantomJS()

driver.maximize_window()

for url in urls:
    print("正在访问{}".format(url))
    try:
        driver.get(url)
        driver.implicitly_wait(10)
        data = driver.page_source
        soup = BeautifulSoup(data, 'lxml')
        hrefs = soup.find_all('a', class_="view_img_link")
    except:
        print("访问异常！")
        continue

    print("开始下载")
    for href in hrefs:
        img = href.get('href')
        img = "http:" + img
        if img[-3:] != 'jpg':
            continue
        print("正在下载第{}张图片".format(x))
        urllib.request.urlretrieve(img, 'F:\\Picture\\%s' % (img.split('/')[-1]))
        x = x + 1
