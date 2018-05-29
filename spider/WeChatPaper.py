import re

import pyquery


def weixin_article_html_parser(html):
    """
    解析微信文章，返回包含文章主体的字典信息
    :param html: 文章HTML源代码
    :return:
    """

    pq = pyquery.PyQuery(html)

    article = {
        "weixin_id": pq.find("#js_profile_qrcode "
                             ".profile_inner .profile_meta").eq(0).find("span").text().strip(),
        "weixin_name": pq.find("#js_profile_qrcode .profile_inner strong").text().strip(),
        "account_desc": pq.find("#js_profile_qrcode .profile_inner "
                                ".profile_meta").eq(1).find("span").text().strip(),
        "article_title": pq.find("title").text().strip(),
        "article_content": pq("#js_content").remove('script').text().replace(r"\r\n", ""),
        "is_orig": 1 if pq("#copyright_logo").length > 0 else 0,
        "article_source_url": pq("#js_sg_bar .meta_primary").attr('href') if pq(
            "#js_sg_bar .meta_primary").length > 0 else '',

    }

    # 使用正则表达式匹配页面中js脚本中的内容
    match = {
        "msg_cdn_url": {"regexp": "(?<=\").*(?=\")", "value": ""},  # 匹配文章封面图
        "var ct": {"regexp": "(?<=\")\d{10}(?=\")", "value": ""},  # 匹配文章发布时间
        "publish_time": {"regexp": "(?<=\")\d{4}-\d{2}-\d{2}(?=\")", "value": ""},  # 匹配文章发布日期
        "msg_desc": {"regexp": "(?<=\").*(?=\")", "value": ""},  # 匹配文章简介
        "msg_link": {"regexp": "(?<=\").*(?=\")", "value": ""},  # 匹配文章链接
        "msg_source_url": {"regexp": "(?<=').*(?=')", "value": ""},  # 获取原文链接
        "var biz": {"regexp": "(?<=\")\w{1}.+?(?=\")", "value": ""},
        "var idx": {"regexp": "(?<=\")\d{1}(?=\")", "value": ""},
        "var mid": {"regexp": "(?<=\")\d{10,}(?=\")", "value": ""},
        "var sn": {"regexp": "(?<=\")\w{1}.+?(?=\")", "value": ""},
    }
    count = 0
    for line in html.split("\n"):
        for item, value in match.items():
            if item in line:
                m = re.search(value["regexp"], line)
                if m is not None:
                    count += 1
                    match[item]["value"] = m.group(0)
                break
        if count >= len(match):
            break

    article["article_short_desc"] = match["msg_desc"]["value"]
    article["article_pos"] = int(match["var idx"]["value"])
    article["article_post_time"] = int(match["var ct"]["value"])
    article["article_post_date"] = match["publish_time"]["value"]
    article["article_cover_img"] = match["msg_cdn_url"]["value"]
    article["article_source_url"] = match["msg_source_url"]["value"]
    article["article_url"] = "https://mp.weixin.qq.com/s?__biz={biz}&mid={mid}&idx={idx}&sn={sn}".format(
        biz=match["var biz"]["value"],
        mid=match["var mid"]["value"],
        idx=match["var idx"]["value"],
        sn=match["var sn"]["value"],
    )

    return article


if __name__ == '__main__':
    from pprint import pprint
    import requests

    url = ("https://mp.weixin.qq.com/s?__biz=MzI1NjA0MDg2Mw==&mid=2650682990&idx=1"
           "&sn=39419542de39a821bb5d1570ac50a313&scene=0#wechat_redirect")
    pprint(weixin_article_html_parser(requests.get(url).text))

# {'account_desc': '夜听，让更多的家庭越来越幸福。',
#  'article_content': '文字：安梦 \xa0 \xa0 声音：刘筱 得到了什么？又失去了什么？',
#  'article_cover_img': 'http://mmbiz.qpic.cn/mmbiz_jpg/4iaBNpgEXstYhQEnbiaD0AwbKhmCVWSeCPBQKgvnSSj9usO4q997wzoicNzl52K1sYSDHBicFGL7WdrmeS0K8niaiaaA/0?wx_fmt=jpeg',
#  'article_pos': 1,
#  'article_post_date': '2017-07-02',
#  'article_post_time': 1499002202,
#  'article_short_desc': '周日    来自刘筱的晚安问候。',
#  'article_source_url': '',
#  'article_title': '【夜听】走到这里',
#  'article_url': 'https://mp.weixin.qq.com/s?__biz=MzI1NjA0MDg2Mw==&mid=2650682990&idx=1&sn=39419542de39a821bb5d1570ac50a313',
#  'is_orig': 0,
#  'weixin_id': 'yetingfm',
#  'weixin_name': '夜听'}
