# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
from scrapy.selector import Selector

from bs4 import BeautifulSoup

#  ----------------
# HACK !!!! Standart import does not work
from .. import items
#  ----------------


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["news.google.ru"]
    start_urls = (
        'http://www.news.google.ru/',
    )

    def parse(self, response):

        # page = Selector(response)
        # content = page.xpath('//div[@class="section-content"]')
        # blocks = content.xpath('//div[@class="esc-body"]') #[0].xpath('//h2[@class="esc-lead-article-title"]/a')


        soup = BeautifulSoup(response.body, 'html.parser')
        blocks = soup.find_all("div", attrs={"class": "esc-body"})

        # blocks = page.xpath('//div[@class="esc-body"]') #[0].xpath('//h2[@class="esc-lead-article-title"]/a')

        for item in blocks:
            publication = items.Publication()

            a = item.find("a", attrs={'class': 'article'})

            url = a['href']
            title = item.find("a", attrs={'class': 'article'}).get_text()
            description = item.find("div", attrs={'class': 'esc-lead-snippet-wrapper'}).next

            # cell = item.xpath('//div[@class="esc-body"]/div/table[@class="esc-layout-table"]/tbody/tr/td[@class="esc-layout-article-cell"]')
            # title = cell.xpath('//div/h2/a/span/text()').extract()[0]
            # url = cell.xpath('//div/h2/a/@href').extract()[0]
            # description = cell.xpath('//div[@class="esc-lead-snippet-wrapper"]/text()').extract()[0]
            publication['title'] = title
            publication['url'] = url
            publication['description'] = description


            yield publication

        """
        POSSIBLE to use BeautifulSoup to extract russian text
        """
        # item['title'] = question.xpath(
        #     'a[@class="question-hyperlink"]/text()').extract()[0]
        # item['url'] = question.xpath(
        #     'a[@class="question-hyperlink"]/@href').extract()[0]
        # yield item

        # return publication


