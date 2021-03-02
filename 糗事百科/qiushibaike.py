# 使用正则爬去糗事百科热图

import urllib.request
import urllib.parse
import re
import os
import time

from crawlab import save_item


def handle_request(url, page):
    url = url + str(page)
    # print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=headers)
    return request


# <img src="//pic.qiushibaike.com/system/pictures/12403/124038509/medium/NZBPUGX352ZNYZDH.jpg" alt="糗事#124038509" class="illustration" width="100%" height="auto">
def save_content(content):
    # 标题列表
    pattern1 = re.compile(
        r'<div class="content">.*?<span>(.*?)</span>.*?</div>', re.S)
    # 图片列表
    pattern2 = re.compile(
        r'<div class="thumb">.*?<img src="(.*?)" .*?>.*?</div>', re.S)
    lt1 = pattern1.findall(content)
    lt2 = pattern2.findall(content)
    # print(lt1)
    # 遍历列表，依次下载图片
    for title, image_src in zip(lt1, lt2):
        # 标题
        title = title.replace('\n', '')
        # 图片链接
        image_src = 'https:' + image_src
        # print(title)
        # print(image_src)
        # 保存数据
        result = {'title': title, 'image_src': image_src}
        save_item(result)
        time.sleep(0.5)


def main():
    url = 'https://www.qiushibaike.com/imgrank/page/'
    # start_page = int(input('请输入起始页码:'))
    # end_page = int(input('请输入结束页码:'))
    for page in range(1, 11):
        print('第%s页开始下载....' % page)
        # 生成请求对象
        request = handle_request(url, page)
        # 发送请求对象，获取响应内容
        content = urllib.request.urlopen(request).read().decode()
        # 解析内容，提取所有的图片链接，下载图片
        save_content(content)
        print('第%s页开始下载结束' % page)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
