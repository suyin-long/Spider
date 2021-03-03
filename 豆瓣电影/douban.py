# 使用jsonpath爬取豆瓣电影排行榜中的动作片(前10页)
# https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20

import json
import urllib.parse
import urllib.request

import jsonpath
from crawlab import save_item


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }
    for page in range(0, 10):
        # https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=20&limit=20
        url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start={}&limit=20'.format(
            page * 20)
        print(url)
        # 发送请求
        request = urllib.request.Request(url=url, headers=headers)
        json_text = urllib.request.urlopen(request).read().decode()
        # 将json格式字符串转化为python对象
        obj = json.loads(json_text)
        # print(obj)
        for movie in obj:
            # print(movie)
            # 电影名称
            name = jsonpath.jsonpath(movie, '$.title')[0]
            print(name)
            # 电影类型
            types = str(jsonpath.jsonpath(movie, '$.types')[0]).strip('[]')
            print(types)
            # 上映时间
            release_date = jsonpath.jsonpath(movie, '$.release_date')[0]
            print(release_date)
            # 制片国家
            regions = str(jsonpath.jsonpath(movie, '$.regions')[0]).strip('[]')
            print(regions)
            # 豆瓣评分
            score = jsonpath.jsonpath(movie, '$.score')[0]
            print(score)
            # 电影主演
            actors = str(jsonpath.jsonpath(movie, '$.actors')[0]).strip('[]')
            print(actors)
            # 保存数据
            result = {
                '电影名称': name,
                '电影类型': types,
                '上映时间': release_date,
                '制片国家': regions,
                '豆瓣评分': score,
                '电影主演': actors
            }
            save_item(result)


if __name__ == '__main__':
    main()
