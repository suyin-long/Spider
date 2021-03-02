# 使用bs4爬取三国演义
# https://www.shicimingju.com/book/sanguoyanyi.html

import urllib.request
import urllib.parse
import time

from bs4 import BeautifulSoup
from crawlab import save_item


def handle_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    return request


# 下载章节内容函数
def download_text(href):
    # 构建请求对象
    request = handle_request(href)
    # 获取网页内容
    content = urllib.request.urlopen(request).read().decode()
    # print(content)
    # exit()
    soup = BeautifulSoup(content, 'lxml')
    # 获取内容
    odiv = soup.find('div', class_="chapter_content")
    return odiv.text


def parse_content(content):
    # 生成一个对象
    soup = BeautifulSoup(content, 'lxml')
    a_list = soup.select('.book-mulu > ul > li > a')
    # print(a_list)
    # print(len(a_list))
    # 遍历这个列表，获取title和href，然后获取内容
    for element in a_list:
        # 根据对象获取内容
        title = element.text
        # 根据对象获取属性
        href = 'http://www.shicimingju.com' + element['href']
        # 根据href获取内容的函数
        print('开始下载---%s' % title)
        text = download_text(href)
        print('结束下载---%s' % title)
        string = title + '\n' + text + '\n'
        # 将标题和内容写入到数据库中
        result = {'title': title, 'content': text}
        save_item(result)
        time.sleep(0.5)


def main():
    url = 'http://www.shicimingju.com/book/sanguoyanyi.html'
    # 构建请求对象
    request = handle_request(url)
    # 发送请求对象，获取响应
    content = urllib.request.urlopen(request).read().decode()
    # 解析内容
    parse_content(content)


if __name__ == '__main__':
    main()
