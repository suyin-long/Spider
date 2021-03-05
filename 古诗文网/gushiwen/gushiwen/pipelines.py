# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings


class MySQLPipeline(object):
    def open_spider(self, spider):
        # 将配置文件读到内存中，是一个字典
        settings = get_project_settings()
        host = settings['DB_HOST']
        port = settings['DB_PORT']
        user = settings['DB_USER']
        password = settings['DB_PASSWORD']
        dbname = settings['DB_NAME']
        dbcharset = settings['DB_CHARSET']

        self.db = pymysql.Connect(host=host, port=port, user=user, password=password, db=dbname, charset=dbcharset)

    def process_item(self, item, spider):
        # 写入数据库中
        sql = 'insert into poems(poem_name, poem_author, author_dynasty, poem_content) values ("%s", "%s", "%s", "%s")' % (
            item['poem_name'], item['poem_author'], item['author_dynasty'], item['poem_content'])
        # 执行sql语句
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)
            print('#' * 60)
            self.db.commit()
        except Exception as e:
            print('=' * 60)
            print(e)
            self.db.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()


class GushiwenPipeline:
    def process_item(self, item, spider):
        return item
