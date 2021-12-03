import scrapy
from scrapy import Request
from learnscrapy.items import LearnscrapyItem
from lxml import etree

class ExampleSpider(scrapy.Spider):
    # def __init__(self):
    #     self.headers =
    name = 'example'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/chart']

    def start_requests(self):

        yield scrapy.Request('https://movie.douban.com/top250', callback=self.parse)

    def parse(self, response):
        # 实例化：转化内容：网页响应内容+本地文件
        base_path = 'https://movie.douban.com/top250'
        html = etree.HTML(response.text)
        movie_detail_urls = html.xpath('//div[@class="hd"]//a/@href')
        for movie_detail_url in movie_detail_urls:
            yield Request(movie_detail_url, callback=self.parse_detail)

        next_url = html.xpath('//span[@class="next"]//a/@href')
        if next_url:
            next_path = base_path+next_url[0]
            yield Request(next_path, callback=self.parse)

    def parse_detail(self, response):
        item = LearnscrapyItem()
        html = etree.HTML(response.text)

        item['title'] = html.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
        contents = ('').join(html.xpath('//*[@id="info"]//text()'))
        for content in contents.split('\n'):
            content = content.replace(' ', '')
            if not content:
                continue
            if '导演' in content:
                item['director'] = content.split(':')[-1]

            if '主演' in content:
                item['actor'] = content.split(':')[-1]

            if '类型' in content:
                item['move_type'] = content.split(':')[-1]

            if '地区' in content:
                item['country'] = content.split(':')[-1]

            if '片长' in content:
                item['time'] = content.split(':')[-1]

        item['rating_num'] = html.xpath('//div[@class="rating_self clearfix"]/strong[@class="ll rating_num"]//text()')[0]
        item['votes'] = html.xpath('//div[@class="rating_sum"]//span/text()')[0]

        yield item
