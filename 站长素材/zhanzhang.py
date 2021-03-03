# 使用XPath爬取站长素材中的性感美女图片(前30页)
# https://sc.chinaz.com/tupian/xingganmeinvtupian.html

import urllib.request
import urllib.parse
import time

from lxml import etree
from crawlab import save_item


def handle_request(url, page):
    # 由于第一页和后面的页码规律不一样，所以要进行判断
    if page == 1:
        url = url.format('')
    else:
        url = url.format('_' + str(page))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=headers)
    return request


# 解析内容，并且下载图片
def parse_content(content):
    tree = etree.HTML(content)
    image_list = tree.xpath('//div[@id="container"]/div/div/a/img')
    for img in image_list:
        # 图片标题
        title = img.xpath('./@alt')[0]
        # 图片链接，懒加载
        img_src = 'https:' + img.xpath('./@src2')[0]
        print(title)
        print(img_src)
        # 保存数据到数据库
        result = {'标题': title, '链接': img_src}
        save_item(result)
        time.sleep(0.5)


def main():
    url = 'https://sc.chinaz.com/tupian/xingganmeinvtupian{}.html'
    # https://sc.chinaz.com/tupian/xingganmeinvtupian.html
    # https://sc.chinaz.com/tupian/xingganmeinvtupian_2.html
    for page in range(1, 31):
        request = handle_request(url, page)
        content = urllib.request.urlopen(request).read().decode()
        parse_content(content)
        time.sleep(1)


if __name__ == '__main__':
    main()
