# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TextItem(scrapy.Item):
    # define the fields for your item here like:
    # 用户头像
    face = scrapy.Field()
    # 用户名
    name = scrapy.Field()
    # 用户年龄
    age = scrapy.Field()
    # 段子内容
    content = scrapy.Field()
    # 好笑个数
    funny = scrapy.Field()
    # 评论个数
    comment = scrapy.Field()
