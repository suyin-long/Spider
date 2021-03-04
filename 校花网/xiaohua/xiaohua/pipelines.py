# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os
import urllib.request


class XiaohuaPipeline:
    def __init__(self):
        self.fp = open('hua.txt', 'w', encoding='utf8')

    def process_item(self, item, spider):
        # 下载图片
        self.download_image(item)
        obj = dict(item)
        string = json.dumps(obj, ensure_ascii=False)
        self.fp.write(string + '\n')
        return item

    def download_image(self, item):
        # 指定下载路径
        dirpath = 'hua'
        if not os.path.exists('hua'):
            os.mkdir('hua')
        file_name = item['title'] + '.jpg'
        filepath = os.path.join(dirpath, file_name)
        urllib.request.urlretrieve(item['img_url'], filepath)

    def close_spider(self, spider):
        self.fp.close()
