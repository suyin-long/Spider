# 使用XPath爬取好段子中的段子
# http://www.haoduanzi.com/wen/

import time
import urllib.request
import urllib.parse

from lxml import etree
from crawlab import save_item


def handle_request(url, page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }
    # 将url和page进行拼接
    url = url.format(page)
    print(url)
    request = urllib.request.Request(url=url, headers=headers)
    return request


def parse_content(content):
    # 生成对象
    tree = etree.HTML(content)
    # 抓取内容
    li_list = tree.xpath('//ul[@class="list-box"]/li')
    # 遍历li列表
    for oli in li_list:
        # 去除是广告的li
        if 'ad' in oli.xpath('./@class'):
            print('#' * 60)
            print('是广告：' + oli.xpath('./@class')[0])
        else:
            print('*' * 60)
            # 获取标题
            title = oli.xpath('./div[@class="head"]/h2/text()')[0]
            print(title)
            text = oli.xpath('./div[@class="content"]/a')[0].xpath('string(.)')
            print(text)
            # 保存内容到数据库
            result = {'标题': title, '内容': text}
            save_item(result)


def main():
    # start_page = int(input('请输入起始页码:'))
    # end_page = int(input('请输入结束页码:'))
    url = 'http://www.haoduanzi.com/category/?1-{}.html'
    for page in range(1, 51):
        request = handle_request(url, page)
        content = urllib.request.urlopen(request).read().decode()
        # 解析内容
        parse_content(content)
        time.sleep(1)


if __name__ == '__main__':
    main()
