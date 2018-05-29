import os

import requests
from bs4 import BeautifulSoup

url = 'https://tieba.baidu.com/p/5316245951'
path = 'F:\\Picture'


def get_pic_name(img_url):
    if not os.path.isdir(path):
        os.mkdir(path)
    return os.path.join(path, str(img_url).split('/')[-1])


if __name__ == '__main__':
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    images = soup.find_all('img', 'BDE_Image')
    for image_tag in images:
        image = image_tag['src']
        print(image)
        image_name = get_pic_name(image)
        with open(image_name, 'wb') as file:
            file.write(requests.get(image).content)
    print('Total image num is : ' + len(images))
