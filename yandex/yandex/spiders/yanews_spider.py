# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
from scrapy import http
from scrapy.utils.response import open_in_browser
import time
import hashlib
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

        # open_in_browser(response)
        """ ------------------------------ """

        soup = BeautifulSoup(response.body, 'html.parser')
        blocks = soup.find("div", attrs={"class": "page-content__left"}).find_all('li', attrs={"class": "search-item"})

        for item in blocks:
            d = ''
            # div = item.find('div', attrs={"class": "document i-bem"})
            li = item.next
            if 'story-item' in li.get('class'):
                # this is subject
                # -> request and parse for SUBJECT!!!!
                try:

                    subject_link = li.find('h2', attrs={'class': 'story-item__title'}).next['href']
                    yield http.Request(self.format_subject_url(subject_link), callback=self.parse_subjects)
                except Exception as e:
                    self.logger.error(e)

            else:
                # this is donor
                # create Donor object and save it
                donor = items.YandexDonor()
                try:
                    title_tag = item.find('div', attrs={'class': 'document__title'}).next
                    donor['link'] = title_tag['href']
                    donor['title'] = title_tag.get_text()
                    donor['description'] = item.find('div', attrs={'class': 'document__snippet'}).get_text()

                    ''' TODO :: Figure out how to parse correct data '''
                    donor['published_at'] = item.find('div', attrs={'class': 'document__time'}).get_text()
                    donor['created_at'] = str(int(time.time()))

                    yield donor
                except Exception as e:
                    self.logger.error(e)

        g = ''

    #     check for next page

    #   request next page
    #     if self.is_next_page_exists(content.get_text()):
    #         self.current_page += 1
    #         yield http.Request('', callback=self.parse)  # crawl SUBJECT and DONORS

        # yield .....SOMETHING FRONT PAGE DONORS

    def parse_subjects(self, response):
        """
        Parse response HTML and create Donor object

        :param response: HtmlResponse
        :return:
        """
        a = ''

        self.save_to_file(response.body, 'subject')
        open_in_browser(response)

        soup = BeautifulSoup(response.body, 'html.parser')

        subject = items.YandexSubject()
        title = soup.find('h1', attrs={'class': 'story__head'})
        subject['title'] = title.get_text()

        #  TODO:: Does not work with cyrillic characters !!
        # subject['title_hash'] = hashlib.md5(subject['title'])

        subject['link'] = response.url
        subject['created_at'] = str(int(time.time()))
        subject['donors_count'] = 0

        try:
            content = soup.find('div', attrs={'class': 'story__main'})
            for item in content.find_all('div', attrs={'class': 'story__group'}):
                donor = items.YandexDonor()

                d_title = item.find('h2', attrs={'class': 'doc__title'})

                donor['title'] = d_title.next.get_text()
                donor['link'] = d_title.next['href']
                donor['description'] = item.find('div', attrs={'class': 'doc__content'}).next.get_text()
                donor['published_at'] = item.find('div', attrs={'class': 'doc__time'}).get_text()

                donor['subject_id'] = hashlib.md5(subject['link']).hexdigest()

                subject['donors_count'] += 1
                yield donor

                # TODO :: Try to yield both objects !!!
                # yield donor, subject

        except Exception as e:
            self.logger.error('Error in parse_subjects method on getting donor. {0}'.format(e))

    @staticmethod
    def is_next_page_exists(html):
        if '<span class="button__text">Следующая</span>' in html:
            return True
        return False

    @staticmethod
    def format_url(search_string='', page=0, only_today=False):
        """
        :param only_today: bool
        :param search_string: str
        :param page: str
        :return: str
        """
        # if ' ' in search_string:
        #     search_string = '+'.join(search_string.split(' '))

        period = ''
        if only_today:
            period = '&within=7'

        return 'https://news.yandex.ru/yandsearch?rpt=nnews2&grhow=clutop&text={0}&rpt=nnews2&rel=rel&numdoc=30&p={1}&noreask=1{2}'.format(search_string, page, period)

    @staticmethod
    def format_subject_url(donor_link):
        return 'https://news.yandex.ru/{0}&content=alldocs'.format(donor_link.strip('/'))

    """ ================================ """

    # DEBUG ONLY
    @staticmethod
    def save_to_file(string, filename='Output'):
        text_file = open("{0}.html".format(filename), "w")
        text_file.write(string)
        text_file.close()
