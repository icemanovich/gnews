# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
from scrapy import http
import time
from bs4 import BeautifulSoup
from .. import items


class KeywordsSpider(scrapy.Spider):
    """
    Parse News.Google by passed keywords
    """

    name = "keywords"
    allowed_domains = ["news.google.ru"]
    start_urls = (
        'http://www.news.google.ru/',
    )

    url_template = ''
    max_pages = 10

    def __init__(self, keywords='', **kwargs):
        super(KeywordsSpider, self).__init__(**kwargs)

        self.keywords = ''
        if len(keywords):
            self.keywords = '+'.join(keywords.split(' '))
        self.start_urls = (
            'https://www.google.ru/search?hl=ru&tbm=nws&authuser=0&gws_rd=cr&q={0}'.format(self.keywords),
        )

    def start_requests(self):
        for i in range(self.max_pages):
            yield http.Request(self.start_urls[0] + '&start={0}0'.format(i), callback=self.parse)

    def parse(self, response):

        soup = BeautifulSoup(response.body, 'html.parser')
        blocks = soup.find("div", attrs={"id": "ires"})

        blocks = blocks.find_all("div", attrs={"class": "g"})

        for item in blocks:
            publication = items.Publication()

            url = ''
            try:
                url = item.find("h3", attrs={'class': 'r'}).next['href'].strip('/url?q=')
                url = url.split('&')[0]
            except IndexError as ie:
                self.log('{0} :: {1}'.format(ie, url))

            title = item.find("h3", attrs={'class': 'r'}).next.get_text()
            description = item.find("div", attrs={'class': 'st'}).get_text()

            publication['title'] = title
            publication['url'] = url
            publication['description'] = description
            publication['updated_at'] = str(int(time.time()))

            yield publication
