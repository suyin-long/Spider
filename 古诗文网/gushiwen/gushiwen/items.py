# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GushiwenItem(scrapy.Item):
    # define the fields for your item here like:
    # 古诗名称
    poem_name = scrapy.Field()
    # 古诗作者
    poem_author = scrapy.Field()
    # 作者朝代
    author_dynasty = scrapy.Field()
    # 古诗内容
    poem_content = scrapy.Field()
