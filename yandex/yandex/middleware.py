import logging

from proxy import PROXIES
from agents import AGENTS
import random
from yandex.statistics import Statistics


class CustomHttpProxyMiddleware(object):
    def process_request(self, request, spider):
        """
        :param request:
        :param spider:
        :return:
        """

        ''' If cookie 'spravka' is missed - set new '''
        request.cookies.update(
            {'spravka':
                 # 'dD0xNDYwNDQ1NjMwO2k9ODIuMjA4Ljk5LjE5Mzt1PTE0NjA0NDU2MzA2ODM5NzEyNzg7aD0xM2U3ZGY4ZTBmNDdmMmQwZjJiZGJkMDkwMzBjNGRmMA',
                 'dD0xNDYxMzIzNTY3O2k9ODIuMjA4Ljk5LjE5Mzt1PTE0NjEzMjM1Njc2NzQ4MjY3Nzc7aD0zMWE4MTIxOWJjOTliMmNhMGZkZDQ5ZjNhODA5OThmYQ',
             })

        # try:
            # request.meta['proxy'] = "http://%s" % p['ip_port']
            # request.meta['proxy'] = 'http://185.2.32.183:1085'
            # request.meta['proxy'] = 'http://192.168.10.102:3030'
        # except Exception as e:
        #     logging.error("Exception CustomHttpProxyMiddleware:: %s" % e, _level=logging.CRITICAL)

        # Statistics.init().send('request.success', 1)

    # def process_response(self, request, response, spider):
    #     d = ''
    #     pass

    @staticmethod
    def process_exception(request, exception, spider):

        d = ''
        spider.logger.error('MIDDLEWARE EXCEPTION CAUGHT')

class CustomUserAgentMiddleware(object):
    """
    Change request headers every time
    """
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(AGENTS)
        request.headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        request.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        request.headers['Connection'] = 'keep-alive'

        ''' ======== '''
        request.headers['Host'] = 'news.yandex.ru'
        request.headers['X-Requested-With'] = 'XMLHttpRequest'
        ''' ======== '''

        Statistics.init().send('request.success', 1)
