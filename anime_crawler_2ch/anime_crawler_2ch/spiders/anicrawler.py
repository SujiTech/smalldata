# -*- coding: utf-8 -*-
import scrapy
from anime_crawler_2ch.items import ThreadItem, PostItem


class AnicrawlerSpider(scrapy.Spider):
    name = 'anicrawler'
    allowed_domains = ['2ch.net']
    start_urls = ['http://rosie.2ch.net/anime/subback.html']

    def parse(self, response):
        for url in response.xpath('//small[@id="trad"]//a/@href').extract():
            aniurl = response.urljoin(url.split('/')[0])
            yield scrapy.Request(url=aniurl, callback=self.parse_anime)
            # break

    def parse_anime(self, response):
        thread = ThreadItem()
        thread['title'] = response.xpath('//h1[@class="title"]/text()').extract_first()
        thread['url'] = response.url
        thread['posts'] = []
        for post in response.xpath('//div[@class="post"]'):
            message = PostItem()
            message['number'] = int(post.xpath('./div[@class="meta"]/span[@class="number"]//text()').extract_first())
            message['name'] = post.xpath('./div[@class="meta"]/span[@class="name"]//text()').extract_first()
            message['date'] = post.xpath('./div[@class="meta"]/span[@class="date"]//text()').extract_first()
            message['uid'] = post.xpath('./div[@class="meta"]/span[@class="uid"]//text()').extract_first()
            message['message'] = " ".join(post.xpath('./div[@class="message"]//text()').extract())
            thread['posts'].append(message)
        return thread
