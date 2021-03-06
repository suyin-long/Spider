# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MzituItem(scrapy.Item):
    # define the fields for your item here like:
    # 图片标题
    title = scrapy.Field()
    # 发布时间
    times = scrapy.Field()
    # 图片链接
    url = scrapy.Field()
