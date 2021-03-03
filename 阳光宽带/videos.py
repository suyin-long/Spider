# 使用selenium+xpath+requests下载视频
# http://365yg.com/

'''
首先向365yg.com发送请求
获取响应，解析响应，将里面所有的标题链接获取到
依次向每个标题链接发送请求
获取响应，解析响应，获取video标签的src属性
向src属性发送请求，获取响应，将内容保存到本地即可
'''
import os
import time
import json
import base64
import urllib.request

import requests
from lxml import etree
from crawlab import save_item
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

'''
接口信息：
http://365yg.com/xigua/feed/?ChannelID=6797027941&Count=10&UseHQ=true
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
}

# 创建一个参数对象，用来控制chrome以无界面模式打开
firefox_options = Options()
# 以无界面模式运行Chrome
firefox_options.add_argument('--headless')
# --disable-gpu 主要是为了屏蔽现阶段可能触发的错误
firefox_options.add_argument('--disable-gpu')
# 设置界面最大化
firefox_options.add_argument('--start-maximized')


def handle_href(title_url, title):
    if not os.path.exists('videos'):
        os.mkdir('videos')
    filename = 'videos/' + title.replace('?', '') + '.mp4'
    # 通过selenium来进行解决
    if 'toutiao' in title_url:
        # 模拟创建一个浏览器对象，然后通过对象去操作浏览器
        browser = webdriver.Firefox(options=firefox_options)
        browser.get(title_url)
        time.sleep(2)
        # 获取源码，生成tree对象，然后查找video里面的src属性
        tree = etree.HTML(browser.page_source)
        browser.save_screenshot('video.png')
        browser.quit()
        # 获取src属性
        video_src = tree.xpath('//video/@src')[0]
        if 'blob:' in video_src:
            print(video_src)
            print('分段视频跳过......')
        else:
            video_src = 'https:' + video_src
            print(video_src)
            # 下载视频
            r = requests.get(url=video_src, headers=headers)
            print(f'{title}开始下载......')
            with open(filename, 'wb')as fp:
                fp.write(r.content)
            print(f'{title}结束下载......')
    else:
        print(f'{title}开始下载......')
        urllib.request.urlretrieve(title_url, filename)
        print(f'{title}结束下载......')
    print('=' * 60)


def handle_title():
    # 将捕获接口拿过来
    url = 'http://365yg.com/xigua/feed/?ChannelID=6797027941&Count=10&UseHQ=true'
    r = requests.get(url, headers=headers)
    # 获取数据
    data = r.json()['Data']
    # print(data)
    print(f'该页共{len(data)}条数据！')
    for item in data:
        # 获取base64加密后的内容
        b64 = item['raw_data']
        # print(b64)
        # 解密base64加密的内容
        content = base64.b64decode(b64).decode('utf8')
        # print(content)
        # 将json数据转化为python对象
        obj = json.loads(content)
        # 获取标题
        title = obj['title']
        print(title)
        # 获取标题链接
        title_url = obj['article_url']
        print(title_url)
        print('*' * 50)
        handle_href(title_url, title)


def main():
    page_number = int(input('请输入想爬取多少页：'))
    for page in range(page_number):
        # 解析首页，返回所有的标题链接
        handle_title()
        time.sleep(1)


if __name__ == '__main__':
    main()
