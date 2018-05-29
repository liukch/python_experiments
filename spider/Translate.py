import requests
from bs4 import BeautifulSoup

# get word from Command line
word = input("Enter a word (enter 'q' to exit): ")

# main body
while word != 'q':  # 'q' to exit
    try:
        # 利用GET获取输入单词的网页信息
        r = requests.get(url='http://dict.youdao.com/w/%s/#keyfrom=dict2.top' % word)
        # 利用BeautifulSoup将获取到的文本解析成HTML
        soup = BeautifulSoup(r.text, "lxml")
        # 获取音标
        phonetics = soup.find_all(class_='phonetic', limit=2)
        phoneticList = []
        for phonetic in phonetics:
            phoneticList.append(phonetic.text)
        print(', '.join(phoneticList))
        # 获取字典的标签内容
        s = soup.find(class_='trans-container')('ul')[0]('li')
        # 输出字典的具体内容
        for item in s:
            if item.text:
                print(item.text)
        print('=' * 35 + '\n')
    except Exception:
        print("Sorry, can't find %s!\n" % word)
    finally:
        word = input("Enter a word (enter 'q' to exit): ")
