# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time
import urllib
import scrapy
import hashlib
from .. import items
from scrapy import http
from bs4 import BeautifulSoup
from scrapy.utils.response import open_in_browser

from yandex.exceptions import YandexBan
# from yandex.yandex.exceptions import YandexMockupError


class YanewsSpider(scrapy.Spider):
    """
    Parse News.Yandex by passed keywords
    """
    name = "yanews"
    allowed_domains = ["news.yandex.ru"]
    start_urls = (
        'http://www.news.yandex.ru/',
    )

    DEBUG = False
    keywords = ''
    max_pages = 10
    current_page = 0

    def __init__(self, keywords='', **kwargs):
        super(YanewsSpider, self).__init__(**kwargs)

        self.keywords = 'клименко и ири'
        # self.keywords = keywords
        self.start_urls = (
            self.format_url(self.keywords, self.current_page),
        )
        self.logger.info('Scrap by keywords: |{0}|'.format(self.keywords))

    def start_requests(self):
        yield http.Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        """
        :param response: HtmlResponse
        :rtype:
        """
        self.logger.info('Crawl url :: {0}'.format(response.url))

        if self.DEBUG:
            self.save_to_file(response.body)
            open_in_browser(response)

        try:
            soup = BeautifulSoup(response.body, 'html.parser')

            '''
            Check if this page is not blocked (captcha)
            '''
            if self.is_page_with_captcha(soup):
                # TODO: auth and request again
                raise YandexBan('Yandex BAN page with captcha')

            blocks = soup.find("div", attrs={"class": "page-content__left"}) \
                .find_all('li', attrs={"class": "search-item"})

            for item in blocks:
                li = item.next
                if 'story-item' in li.get('class'):
                    '''
                    Detect Subject and go into it to crawl donors
                    '''
                    try:
                        subject_link = li.find('h2', attrs={'class': 'story-item__title'}).next['href']
                        yield http.Request(self.format_subject_url(subject_link), callback=self.parse_subjects)
                    except AttributeError as e_attr:
                        self.logger.error('Error to get HTML content in outer Subject page :: {0}'.format(e_attr))

            ''' request next page '''
            content_block = soup.find('div', attrs={'class': 'page-content__left'})
            if self.is_next_page_exists(content_block):
                self.current_page += 1

                ''' Limit pages scan '''
                if self.max_pages >= self.current_page:
                    '''crawl SUBJECT and DONORS '''
                    yield http.Request(self.format_url(self.keywords, self.current_page), callback=self.parse)

        except ValueError as e_value:
            self.logger.info('Page skip :: {0}'.format(e_value))
        except YandexBan as e_ya:
            self.logger.warning('Yandex Ban your request :: {0}'.format(e_ya))
        except Exception as e:
            self.logger.info('Global exception - [type{0}] :: {0}'.format(type(e).__name__, e))
            import traceback
            traceback.print_exc()
            # open_in_browser(response)

    def parse_subjects(self, response):
        """
        Parse response HTML and create Donor object

        :param response: HtmlResponse
        :return:
        """
        if self.DEBUG:
            self.save_to_file(response.body, 'subject')
            open_in_browser(response)

        try:
            soup = BeautifulSoup(response.body, 'html.parser')

            subject = items.YandexSubject()
            subject['title'] = soup.find('h1', attrs={'class': 'story__head'}).next.get_text()

            #  TODO:: Does not work with cyrillic characters !!
            # subject['title_hash'] = hashlib.md5(subject['title'])

            subject['link'] = urllib.unquote(response.url).decode('utf8')
            ''' Link to Yandex referrer to '''
            subject['link_target'] = urllib.unquote(self.extract_external_link(response.url)).decode('utf8')
            subject['link_hash'] = self.hash_link(subject['link'])

            subject['created_at'] = str(int(time.time()))
            subject['donors_count'] = 0
            subject['keywords'] = self.keywords

            content = soup.find('div', attrs={'class': 'story__main'})
            for item in content.find_all('div', attrs={'class': 'story__group'}):
                donor = items.YandexDonor()

                d_title = item.find('h2', attrs={'class': 'doc__title'})

                donor['title'] = d_title.next.get_text()
                donor['link'] = urllib.unquote(d_title.next['href']).decode('utf8')
                donor['link_hash'] = self.hash_link(donor['link'])
                donor['description'] = item.find('div', attrs={'class': 'doc__content'}).next.get_text()
                donor['published_at'] = item.find('div', attrs={'class': 'doc__time'}).get_text()

                donor['subject_id'] = subject['link_hash']
                donor['keywords'] = self.keywords

                subject['donors_count'] += 1
                yield donor

            yield subject

        except Exception as e:
            self.logger.error('Error in parse_subjects method on getting donor. {0}'.format(e))

    @staticmethod
    def is_next_page_exists(content):
        """ Check if HTML contains page counter for further pages

        :param content: Tag
        :return:
        """
        # if '<span class="button__text">Следующая</span>' in html:
        #     return True

        counter_block = content.find_all('span', attrs={'class': 'pager__group'})
        if len(counter_block[-1].contents) == 1:
            return True
        return False

    @staticmethod
    def is_page_with_captcha(soup):
        """
        Check if captcha form contains on page
        :param soup: BeautifulSoup
        :rtype: bool
        """
        captcha = soup.find('form', attrs={'action': '/checkcaptcha'})
        if captcha is None:
            return False
        return True

    @staticmethod
    def format_url(search_string='', page=0, only_today=False):
        """
        :param only_today: bool
        :param search_string: str
        :param page: str
        :return: str
        """
        period = ''
        if only_today:
            period = '&within=7'

        return 'https://news.yandex.ru/yandsearch?rpt=nnews2&grhow=clutop&text={0}&rpt=nnews2&rel=rel&numdoc=30&p={1}&noreask=1{2}'.format(
            search_string, page, period)

    @staticmethod
    def format_subject_url(donor_link):
        return 'https://news.yandex.ru/{0}&content=alldocs'.format(donor_link.strip('/'))

    @staticmethod
    def extract_external_link(url):
        """ Return external donor link from yandex search string """

        url = url.replace('https://news.yandex.ru/yandsearch?cl4url=', '')
        return url[:url.index('&')]

    @staticmethod
    def hash_link(link):
        return hashlib.md5(link).hexdigest()

    """ ================================ """

    # DEBUG ONLY
    @staticmethod
    def save_to_file(string, filename='Output'):
        text_file = open("tmp/{0}.html".format(filename), "w")
        text_file.write(string)
        text_file.close()
