# -*- encoding:utf-8 -*-
import douban_crawl
import traceback


def simple_reply(msg):
    global movie_info_all
    if u'电影' in msg:
        douban_object.browser_hotopen()
        movie_category_option = ' '.join(douban_crawl.movie_category)
        print('----请选择一种类型----\n' + movie_category_option)

    elif msg in douban_crawl.movie_category:
            print('正在查找' + msg + '电影...')
            del douban_crawl.command_cache[:]
            douban_crawl.command_cache.append(msg)
            movie_info_all = douban_object.browser_action_general_info(msg)
            print('----按热度排序----\n' + '\n' + '\n'.join(douban_crawl.movie_info_hot))
            print('----按时间排序----\n' + '\n' + '\n'.join(douban_crawl.movie_info_time))
            print('----按评论排序----\n' + '\n' + '\n'.join(douban_crawl.movie_info_comment))

    else:
        search_num = 0
        for x in movie_info_all:
            if msg in x:
                print('正在查找' + msg + '...')
                loc = movie_info_all.index(x)
                if 0 <= loc < 10:
                    search_num = 1
                elif 10 <= loc < 20:
                    search_num = 2
                else:
                    search_num = 3
                break
        url_result = douban_object.get_movie_url(msg)
        if not url_result:
            print('没找到这么个电影')
            return
        html_result = douban_object.download_detail_info_html(url_result)
        try:
            douban_object.parse_detail_info(html_result)
        except Exception as e:
            print(e)
            # traceback.print_exc()
            print('您输入的好像是一名演员')
            return
        print('\n\n'.join(douban_crawl.movie_detail_info))


if __name__ == '__main__':
    movie_info_all = []
    msg = input('Enter key words: ')
    douban_object = douban_crawl.DoubanSpider()
    while msg != 'q':
        simple_reply(msg)
        msg = input('Enter key words: ')

