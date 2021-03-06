# 使用CrawlSpider爬取古诗文网中的古诗词
# 使用两个管道：MySQL和MongoDB
# https://www.gushiwen.cn/


import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import GushiwenItem


class PoemSpider(CrawlSpider):
    name = 'poem'
    allowed_domains = ['www.gushiwen.cn', 'so.gushiwen.cn']
    start_urls = ['https://so.gushiwen.cn/shiwens/']

    rules = (
        # 获取朝代连接列表
        Rule(LinkExtractor(allow=r'/shiwens/default.aspx\?cstr=.*'), follow=True),
        # 获取所有的页码列表
        Rule(LinkExtractor(allow=r'/shiwens/default.aspx\?page=.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 创建item对象
        item = GushiwenItem()
        print('*' * 60)
        print(response.url)
        # 获取所有div列表
        div_list = response.xpath('//div[@id="leftZhankai"]/div[@class="sons"]')
        # 遍历div_list
        for odiv in div_list:
            print('+' * 60)
            # 古诗名称
            item['poem_name'] = odiv.xpath('./div[1]/p[1]/a/b/text()').get()
            print(item['poem_name'])
            # 古诗作者
            item['poem_author'] = odiv.xpath('./div[1]/p[2]/a[1]/text()').get()
            print(item['poem_author'])
            # 作者朝代
            item['author_dynasty'] = odiv.xpath('./div[1]/p[2]/a[2]/text()').get()
            print(item['author_dynasty'])
            # 古诗内容
            item['poem_content'] = odiv.xpath('./div[1]/div[2]')[0].xpath('string(.)').get().strip('\n\t ')
            print(item['poem_content'])
            yield item
        print('*' * 60)
