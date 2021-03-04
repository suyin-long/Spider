# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class TextPipeline:
    # 重写这个方法，当爬虫开启的时候就会调用这个方法
    def open_spider(self, spider):
        self.fp = open('qiubai.txt', 'w', encoding='utf8')

    # 处理item数据的方法
    def process_item(self, item, spider):
        # 将item保存到文件中
        self.fp.write(json.dumps(dict(item), ensure_ascii=False) + '\n')
        return item

    # 当爬虫结束时候调用这个方法
    def close_spider(self, spider):
        self.fp.close()
