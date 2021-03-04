# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaohuaItem(scrapy.Item):
    # define the fields for your item here like:
    # 图片标题
    title = scrapy.Field()
    # 图片链接
    img_url = scrapy.Field()
