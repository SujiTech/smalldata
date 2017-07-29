# -*- coding: utf-8 -*-
import scrapy


class AnicrawlerSpider(scrapy.Spider):
    name = 'anicrawler'
    allowed_domains = ['2ch.net']
    start_urls = ['http://rosie.2ch.net/anime/subback.html']

    def parse(self, response):
        for url in response.xpath('//small[@id="trad"]//a/@href').extract():
            print(url)

