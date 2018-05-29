#!/usr/bin/env python3
# encoding: utf-8
import time
from urllib import parse

from pyquery import PyQuery
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def weibo_user_search(url):

    desired_capabilities = DesiredCapabilities.CHROME.copy()
    desired_capabilities["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                 "Chrome/59.0.3071.104 Safari/537.36")
    desired_capabilities["phantomjs.page.settings.loadImages"] = True
    # 自定义头部
    desired_capabilities["phantomjs.page.customHeaders.Upgrade-Insecure-Requests"] = 1
    desired_capabilities["phantomjs.page.customHeaders.Cache-Control"] = "max-age=0"
    desired_capabilities["phantomjs.page.customHeaders.Connection"] = "keep-alive"

    driver = webdriver.PhantomJS(
        desired_capabilities=desired_capabilities,
        service_log_path="ghostdriver.log", )
    # 设置对象的超时时间
    driver.implicitly_wait(1)
    # 设置页面完全加载的超时时间，包括页面全部渲染，异步同步脚本都执行完成
    driver.set_page_load_timeout(60)
    # 设置异步脚本的超时时间
    driver.set_script_timeout(60)

    driver.maximize_window()
    try:
        driver.get(url=url)
        time.sleep(1)
        try:
            # 打开页面之后做一些操作
            company = driver.find_element_by_css_selector("p.company")
            ActionChains(driver).move_to_element(company)
        except WebDriverException:
            pass
        html = driver.page_source
        pq = PyQuery(html)
        person_lists = pq.find("div.list_person")
        if person_lists.length > 0:
            for index in range(person_lists.length):
                person_ele = person_lists.eq(index)
                print(person_ele.find(".person_name > a.W_texta").attr("title"))
                # span_list = person_ele.find(".person_num > span")
                # for span in span_list:
                #     if span.text == "粉丝":
                #         print("粉丝: $%d" % (span.find(".span > a.W_linkb").text()))
                print(person_ele.find(".person_num > span").eq(1).text())
        return html
    except (TimeoutException, Exception) as e:
        print(e)
    finally:
        driver.quit()


if __name__ == '__main__':
    weibo_user_search(url="http://s.weibo.com/user/%s" % parse.quote("LOL"))
