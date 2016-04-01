# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
from scrapy.selector import Selector

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

        publication = items.Publication()

        page = Selector(response)
        # page.xpath('/html/body/div[3]/div[1]/div/div/div[3]/div/div[1]/table/tbody/tr/td[1]/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]')
        content = page.xpath('//div[@class="section-content"]')
        blocks = content.xpath('//div[@class="esc-body"]') #[0].xpath('//h2[@class="esc-lead-article-title"]/a')

        for item in blocks:
            cell = item.xpath('//div[@class="esc-body"]/div/table[@class="esc-layout-table"]/tbody/tr/td[@class="esc-layout-article-cell"]')

            title = cell.xpath('//div/h2/a/span/text()').extract()[0]
            url = cell.xpath('//div/h2/a/@href').extract()[0]
            description = cell.xpath('//div[@class="esc-lead-snippet-wrapper"]').extract()[0]

            publication['title'] = title
            publication['url'] = url
            publication['description'] = description

            # cell //div[@class="esc-body"]/div/table[@class="esc-layout-table"]/tbody/tr/td[@class="esc-layout-article-cell"]
            # a  //div[@class="esc-body"]/div/table[@class="esc-layout-table"]/tbody/tr/td[@class="esc-layout-article-cell"]/div/h2/a
            #a text = a/span

        """
        POSSIBLE to use BeautifulSoup to extract russian text
        """
        # item['title'] = question.xpath(
        #     'a[@class="question-hyperlink"]/text()').extract()[0]
        # item['url'] = question.xpath(
        #     'a[@class="question-hyperlink"]/@href').extract()[0]
        # yield item

        # return publication
        yield publication
