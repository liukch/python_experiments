# -*- coding: utf-8 -*-
from selenium import webdriver
import csv
import codecs

# 第一页的url
url = 'http://music.163.com/#/discover/playlist'

driver = webdriver.PhantomJS()
csv_file = codecs.open('playlist.csv', 'w', 'utf_8_sig')
writer = csv.writer(csv_file)
writer.writerow(['标题', '播放数', '链接'])

while url != 'javascript:void(0)':

    while True:
        try:
            driver.get(url)
            driver.switch_to.frame("g_iframe")
            data = driver.find_element_by_id(
                'm-pl-container').find_elements_by_tag_name('li')
            for i in range(len(data)):
                nb = data[i].find_element_by_class_name('nb').text
                if '万' in nb and int(nb.split('万')[0]) > 500:
                    msk = data[i].find_element_by_css_selector('a.msk')
                    writer.writerow([
                        msk.get_attribute('title'), nb,
                        msk.get_attribute('href')
                    ])
            break
        except Exception as e:
            print(e)

    url = driver.find_element_by_css_selector('a.zbtn.znxt').get_attribute(
        'href')
    print(url)
csv_file.close()
