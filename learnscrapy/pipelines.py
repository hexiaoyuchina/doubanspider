# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class LearnscrapyPipeline:

    def open_spider(self, spider):
        self.conn = pymysql.connect(host="localhost",
                                    user="root",
                                    password="123456",
                                    database="spider",
                                    charset='utf8')
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute("insert into douban (title,rating_num,votes,move_type,country,time,director,actor)" \
        "values(%s,%s,%s,%s,%s,%s,%s,%s)", (
                                            item['title'],
                                            item['rating_num'],
                                            item['votes'],
                                            item['move_type'],
                                            item['country'],
                                            item['time'],
                                            item['director'],
                                            item['actor'],
                                            ))
        return item
