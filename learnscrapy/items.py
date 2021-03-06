# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,Compose,Join

class LearnscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  # 电影名
    rating_num = scrapy.Field()  # 电影评分
    votes = scrapy.Field()  # 评分人数
    move_type = scrapy.Field()  # 电影类型
    country = scrapy.Field()  # 国家
    time = scrapy.Field()  # 时长
    director = scrapy.Field(output_processor=Join())  # 导演
    actor = scrapy.Field(input_processor=MapCompose(str.strip),output_processor = Join())  # 演员


