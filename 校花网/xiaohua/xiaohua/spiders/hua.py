# 使用Scrapy爬取校花网中的大学校花(前50页)
# http://www.521609.com/daxuexiaohua/

import scrapy
from ..items import XiaohuaItem


class HuaSpider(scrapy.Spider):
    name = 'hua'
    allowed_domains = ['www.521609.com']
    start_urls = ['http://www.521609.com/daxuexiaohua/']

    # 爬取多页
    url = 'http://www.521609.com/daxuexiaohua/list3{}.html'
    page = 1

    def parse(self, response):
        # 创建item对象
        item = XiaohuaItem()
        # 获取所有的li标签
        li_list = response.xpath('//div[@class="index_img list_center"]/ul/li')
        # 遍历li_list
        for oli in li_list:
            print('*' * 60)
            # 图片标题
            item['title'] = oli.xpath('./a[1]/img/@alt').get().strip()
            # 图片链接
            item['img_url'] = 'http://www.521609.com' + oli.xpath('./a[1]/img/@src').get()
            yield item
        print('*' * 60)

        if self.page <= 49:
            self.page += 1
            url = self.url.format(self.page)
            yield scrapy.Request(url, callback=self.parse)
