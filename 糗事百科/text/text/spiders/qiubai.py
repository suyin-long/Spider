# 使用scrapy爬取糗事百科中的段子(前10页)
# https://www.qiushibaike.com/text/

import scrapy
# 导入指定的数据结构
from ..items import TextItem


class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']
    # 爬取多页
    url = 'https://www.qiushibaike.com/text/page/{}/'
    page = 1

    def parse(self, response):
        # 创建对象
        item = TextItem()
        # 首先查找所有的div
        div_list = response.xpath('//div[contains(@id, "qiushi_tag")]')
        # 遍历div_list
        for odiv in div_list:
            print('*' * 60)
            # 用户头像
            face = 'https:' + odiv.xpath('./div[1]/a[1]/img/@src').get()
            print(face)
            # 用户名
            name = odiv.xpath('./div[1]/a[1]/img/@alt').get()
            print(name)
            # 用户年龄
            age = odiv.xpath('./div[1]/div/text()').get()
            print(age)
            # 段子内容
            content = odiv.xpath('./a/div/span')[0].xpath('string(.)').get().strip('\n\t ')
            print(content)
            # 好笑个数
            funny = odiv.xpath('./div[2]/span[1]/i/text()').get()
            print(funny)
            # 评论个数
            comment = odiv.xpath('./div[2]/span[2]/a/i/text()').get()
            print(comment)

            # 将获取的属性放到对象中
            item['face'] = face
            item['name'] = name
            item['age'] = age
            item['content'] = content
            item['funny'] = funny
            item['comment'] = comment
            yield item
        print('*' * 60)

        # 接着发送请求，爬取下一页
        if self.page <= 9:
            self.page += 1
            url = self.url.format(self.page)
            print(url)
            # 向拼接后的URL发送请求
            yield scrapy.Request(url, callback=self.parse)

            # 不能这么做，应该用我们的数据结构
            # item = {
            #     '用户头像': face,
            #     '用户名称': name,
            #     '用户年龄': age,
            #     '用户内容': content,
            #     '好笑个数': funny,
            #     '评论个数': comment
            # }
            # print(item)
