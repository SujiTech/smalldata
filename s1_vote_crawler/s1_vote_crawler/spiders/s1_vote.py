# -*- coding: utf-8 -*-
import scrapy
from s1_vote_crawler.items import ThreadItem, PostItem
import re

class S1Vote(scrapy.Spider):
    name = 'S1Vote'
    allowed_domains = ['saraba1st.com']
    start_urls = ['http://bbs.saraba1st.com/2b/forum-83-1.html']

    def parse(self, response):
        for url in response.xpath('//tbody[contains(@id,"normalthread")]//a[@class="s xst"]/@href').extract():
            aniurl = response.urljoin(url)
            yield scrapy.Request(url=aniurl, callback=self.parse_anime)
            # break
        next_page = response.xpath('//a[@class="nxt"]').extract_first()
        if next_page is not None:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_anime(self, response):
        try:
            thread = response.meta['thread']
        except:
            thread = ThreadItem()
            thread['title'] = response.xpath(
                '//span[@id="thread_subject"]/text()').extract_first()
            thread['url'] = response.url
            thread['vote'] = re.sub("\s+", " ", " ".join(response.xpath(
                '//form[@id="poll"]//table//text()').extract()))
            thread['posts'] = []

        for post in response.xpath('//div[@id="postlist"]/div[contains(@id, "post_")]'):
            message = PostItem()
            try:
                message['number'] = int(post.xpath('.//div[@class="pi"]/strong/a/em//text()').extract_first())
            except:
                message['number'] = 1
            message['name'] = post.xpath(
                './/a[@class="xw1"]//text()').extract_first()
            message['date'] = " ".join(post.xpath(
                './/em[contains(@id, "authorposton")]//text()').extract_first().split(" ")[1:])
            message['uid'] = int(post.xpath(
                './/a[@class="xw1"]/@href').extract_first().split("-")[-1].split(".")[0])
            message['message'] = " ".join(post.xpath(
                './/td[@class="t_f"]//text()').extract())
            thread['posts'].append(message)
            # break

        next_page = response.xpath('//a[@class="nxt"]').extract_first()
        if next_page is not None:
            request = scrapy.Request(url=response.urljoin(
                next_page), callback=self.parse_anime)
            request.meta['thread'] = thread
        else:
            return thread
