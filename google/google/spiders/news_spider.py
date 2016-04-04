# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
from bs4 import BeautifulSoup
import time

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
        soup = BeautifulSoup(response.body, 'html.parser')
        blocks = soup.find_all("div", attrs={"class": "esc-body"})

        for item in blocks:
            publication = items.Publication()

            url = item.find("a", attrs={'class': 'article'})['href']
            title = item.find("a", attrs={'class': 'article'}).get_text()
            description = item.find("div", attrs={'class': 'esc-lead-snippet-wrapper'}).next

            publication['title'] = title
            publication['url'] = url
            publication['description'] = description
            publication['updated_at'] = str(int(time.time()))

            yield publication
