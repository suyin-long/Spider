# 使用多线程+xpath+requests爬取贱图(前50页)
# http://www.ifanjian.net/jiantu

import time
import requests
import threading

from lxml import etree
from queue import Queue
from crawlab import save_item

# 用来存放采集线程
g_crawl_list = []
# 用来存放解析线程
g_parse_list = []


class CrawlThread(threading.Thread):
    def __init__(self, name, page_queue, data_queue):
        super().__init__()
        self.name = name
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.url = 'http://www.ifanjian.net/jiantu-{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'
        }

    def run(self):
        print(f'{self.name}------线程启动')
        while 1:
            # 判断采集线程何时退出
            if self.page_queue.empty():
                break
            # 从队列中取出页码
            page = self.page_queue.get()
            # 拼接url，发送请求
            url = self.url.format(page)
            r = requests.get(url, headers=self.headers)
            # 将响应内容存放在data_queue中
            self.data_queue.put(r.text)
        print(f'{self.name}======线程结束')


class ParserThread(threading.Thread):
    def __init__(self, name, page_queue, data_queue, lock):
        super().__init__()
        self.name = name
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.lock = lock

    def parse_content(self, data):
        tree = etree.HTML(data)
        # 先查找所有的li，在从li里边找自己的标题和url
        li_list = tree.xpath('//ul[@class="cont-list"]/li')
        for oli in li_list:
            print('*' * 60)
            # 获取标题
            title = oli.xpath('./h2/a/text()')[0]
            print(title)
            # 获取图片url，懒加载
            try:
                image_url = oli.xpath('./div[@class="cont-list-main"]/p[2]/img/@data-src')[0]
            except IndexError as e:
                print('#' * 60)
                image_url = oli.xpath('./div[@class="cont-list-main"]/p[2]/img/@src')[0]
                print(image_url)
            else:
                print(image_url)
            result = {
                '标题': title,
                '链接': image_url,
            }
            # 写入数据库
            self.lock.acquire()
            save_item(result)
            self.lock.release()

    def run(self):
        print(f'{self.name}------线程启动')
        while 1:
            # 判断解析线程何时退出
            if self.page_queue.empty():
                time.sleep(5)
                if self.data_queue.empty():
                    break
            # 从data_queue中取出一页数据
            data = self.data_queue.get()
            # print(data)
            # 解析内容
            self.parse_content(data)
            print(f'{self.name}======线程结束')


def create_queue():
    # 创建页码对列
    page_queue = Queue()
    for page in range(1, 51):
        page_queue.put(page)

    # 创建内容对列
    data_queue = Queue()
    return page_queue, data_queue


# 创建采集线程
def create_crawl_thread(page_queue, data_queue):
    crawl_name = ['采集线程1号', '采集线程2号', '采集线程3号']
    for name in crawl_name:
        # 创建一个采集线程
        tcrawl = CrawlThread(name, page_queue, data_queue)
        # 保存到列表中
        g_crawl_list.append(tcrawl)


# 创建解析线程
def create_parse_thread(page_queue, data_queue, lock):
    parse_name = ['解析线程1号', '解析线程2号', '解析线程3号']
    for name in parse_name:
        # 创建一个解析线程
        tparse = ParserThread(name, page_queue, data_queue, lock)
        # 保存到列表中
        g_parse_list.append(tparse)


def main():
    # 创建对列函数
    page_queue, data_queue = create_queue()
    # 创建锁
    lock = threading.Lock()
    # 创建采集线程
    create_crawl_thread(page_queue, data_queue)
    # 创建解析线程
    create_parse_thread(page_queue, data_queue, lock)
    # 启动所有采集线程和解析线程
    for tcrawl, tparse in zip(g_crawl_list, g_parse_list):
        tcrawl.start()
        tparse.start()
    # 让主线程等待子线程结束再结束
    for tcrawl, tparse in zip(g_crawl_list, g_parse_list):
        tcrawl.join()
        tparse.join()
    print('主线程和子线程全部结束')


if __name__ == '__main__':
    main()
