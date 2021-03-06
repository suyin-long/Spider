# 使用CrawlSpider爬取妹子图网站上的图片
# 主页图片没有防盗链，但却是懒加载；详情页图片有防盗链
# 使用了两个管道：MySQL和MongoDB
# https://www.mzitu.com/
import os

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import MzituItem


class TuSpider(CrawlSpider):
    name = 'tu'
    allowed_domains = ['www.mzitu.com', 'imgpc.iimzt.com']
    start_urls = ['https://www.mzitu.com/']

    rules = (
        # 首页页码
        Rule(LinkExtractor(restrict_xpaths='//div[@class="nav-links"]/a'), callback='parse_item', follow=True),
        # 详情页链接
        # Rule(LinkExtractor(restrict_xpaths='//ul[@id="pins"]/li/a'), follow=True),
        # 详情页页码
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="pagenavi"]/a'), callback='parse_detail', follow=True),
    )

    def parse_item(self, response):
        # 创建item对象
        item = MzituItem()
        # 获取li标签列表
        li_list = response.xpath('//ul[@id="pins"]/li')
        # 遍历li_list
        for oli in li_list:
            print('*' * 60)
            # 图片标题
            item['title'] = oli.xpath('./a/img/@alt').get()
            print(item['title'])
            # 发布时间
            item['times'] = oli.xpath('./span[@class="time"]/text()').get()
            print(item['times'])
            # 图片链接(懒加载)
            item['url'] = oli.xpath('./a/img/@data-original').get()
            print(item['url'])
            yield item

    def parse_detail(self, response):
        print('-' * 60)
        print(response.url)
        # 图片标题
        title = response.xpath('//h2/text()').get()
        print(title)
        # 图片链接
        url = response.xpath('//div[@class="main-image"]/p/a/img/@src').get()
        print(url)

        if url:
            # 下载防盗链图片
            yield scrapy.Request(url, callback=self.download, cb_kwargs={'title': title})

    # 下载防盗链图片，referer会自动添加
    def download(self, response, title):
        print('<' * 60)
        dirpath = r'C:\Users\suyin\Desktop\test\mzitu'
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        # 图片名称
        image_name = title + '.jpg'
        print(image_name)
        # 图片路径
        image_path = os.path.join(dirpath, image_name)
        # 下载图片
        with open(image_path, 'wb') as fp:
            fp.write(response.body)
        print('>' * 60)
