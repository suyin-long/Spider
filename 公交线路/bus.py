# 使用requests+xpath爬取新乡公交线路
# https://xinxiang.8684.cn/

import time

import requests
from lxml import etree
from crawlab import save_item

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'
}


def parse_navigation():
    url = 'https://xinxiang.8684.cn/'
    r = requests.get(url, headers=headers)
    # 解析内容，获取所有的导航链接
    tree = etree.HTML(r.text)
    # 查找以数字开头的所有链接
    number_href_list = tree.xpath('//div[@class="bus-layer depth w120"]/div[1]/div/a/@href')
    # 查找以字母开头的所有链接
    char_href_list = tree.xpath('//div[@class="bus-layer depth w120"]/div[2]/div/a/@href')
    # 将需要爬取的所有连接返回
    return number_href_list + char_href_list


def parse_sanji_route(content):
    tree = etree.HTML(content)
    # 获取公交线路信息
    bus_number = tree.xpath('//h1/text()')[0]
    print(f'开始爬取{bus_number}公交信息......')
    # 获取运行时间
    run_time = tree.xpath('//ul[@class="bus-desc"]/li[1]/text()')[0].replace('运行时间：', '')
    # 获取票价信息
    ticket_info = tree.xpath('//ul[@class="bus-desc"]/li[2]/text()')[0].replace('票价信息：', '')
    # 获取更新时间
    update_time = tree.xpath('//ul[@class="bus-desc"]/li[4]/text()')[0].replace('最后更新：', '')
    # 获取上行总站数
    up_total = tree.xpath('//div[@class="total"]/text()')[0]
    # 获取上行所有站名
    up_site_list = tree.xpath('//div[@class="bus-lzlist mb15"][1]/ol/li/a/text()')
    # 获取下行总站数
    try:
        down_total = tree.xpath('//div[@class="total"]/text()')[1]
    except IndexError as e:
        print(e)
        down_total = 'None'
        down_site_list = []
    else:
        # 获取下行所有站名
        down_site_list = tree.xpath('//div[@class="bus-lzlist mb15"][2]/ol/li/a/text()')
    # 将每一条公交的线路信息存放到字典中
    result = {
        '线路名': bus_number,
        '运行时间': run_time,
        '票价信息': ticket_info,
        '更新时间': update_time,
        '上行站数': up_total,
        '上行站点': up_site_list,
        '下行站数': down_total,
        '下行站点': down_site_list,
    }
    save_item(result)
    print(f'{bus_number}公交信息爬取结束......')
    print('=' * 60)
    time.sleep(1)


def parse_erji_route(content):
    tree = etree.HTML(content)
    # 获取每一个线路
    route_list = tree.xpath('//div[@class="list clearfix"]/a/@href')
    # 遍历上面这个列表
    for route in route_list:
        route = 'https://xinxiang.8684.cn' + route
        print(route)
        r = requests.get(url=route, headers=headers)
        # 解析内容，获取每一路公交的详细信息
        parse_sanji_route(r.text)


def parse_erji(navi_list):
    # print(navi_list)
    # 遍历上面的列表，依次发送请求，解析内容，获取每一个页面所有的公交路线url
    for first_url in navi_list:
        url = 'https://xinxiang.8684.cn' + first_url
        print(url)
        r = requests.get(url, headers=headers)
        # 解析内容，获取每一路公交的详细url
        parse_erji_route(r.text)


def main():
    # 爬取第一页所有的导航链接
    navi_list = parse_navigation()
    # 爬取二级页面，需要找到以1开头的所有公交路线
    parse_erji(navi_list)


if __name__ == '__main__':
    main()
