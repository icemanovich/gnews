# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
from scrapy import http
import time
from bs4 import BeautifulSoup
from .. import items


class YanewsSpider(scrapy.Spider):
    """
    Parse News.Yandex by passed keywords
    """
    name = "yanews"
    allowed_domains = ["news.yandex.ru"]
    start_urls = (
        'http://www.news.yandex.ru/',
    )

    max_pages = 10
    current_page = 0

    def __init__(self, keywords='', **kwargs):
        super(YanewsSpider, self).__init__(**kwargs)

        self.keywords = keywords

        self.start_urls = (
            self.format_url(self.keywords, self.current_page),
        )

    def start_requests(self):
        self.logger.warning('RUN START_REQUESTS')
        yield http.Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):

        self.logger.warning('Craws url :: {0}'.format(response.url))
        self.save_to_file(response.body)

        soup = BeautifulSoup(response.body, 'html.parser')
        content = soup.find("div", attrs={"class": "page-content__left"})

        blocks = content.find_all('li', attrs={"class": "search-item"})

        for item in blocks:
            d = ''
            # div = item.find('div', attrs={"class": "document i-bem"})
            if item.has_attr('id'):
                # this is subject
                # -> request and parse for SUBJECT!!!!
                pass
            else:
                # this is donor
                #cretae Donor object and save it
                pass


        g = ''

    #     check for next page

    #   request next page
    #     if self.is_next_page_exists(content.get_text()):
    #         self.current_page += 1
    #         yield http.Request('', callback=self.parse_subject)  # crawl SUBJECT and DONORS

        # yield .....SOMETHING FRONT PAGE DONORS


    def is_next_page_exists(self, html):

        if '<span class="button__text">Следующая</span>' in html:
            return True

        return False








        # yield Someth


    #     parse page
    #     get subjects - > request it
    #     get donors -> request it


    def parse_subjects(self, response):
        pass

    def parse_donors(self, response):
        pass

    def extract_subject_link(self):
        pass

    def extract_donor_link(self):
        pass



    @staticmethod
    def format_url(search_string='', page=0):
        """

        :param search_string: str
        :param page: str
        :return: str
        """
        # if ' ' in search_string:
        #     search_string = '+'.join(search_string.split(' '))

        return 'https://news.yandex.ru/yandsearch?rpt=nnews2&grhow=clutop&text={0}&rpt=nnews2&rel=rel&numdoc=30&p={1}&noreask=1'.format(search_string, page)

    # DEBUG ONLY
    @staticmethod
    def save_to_file(string):
        text_file = open("Output.html", "w")
        text_file.write(string)
        text_file.close()
