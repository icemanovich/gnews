from proxy import PROXIES
from agents import AGENTS
import logging
import random


class CustomHttpProxyMiddleware(object):
    def process_request(self, request, spider):
        p = random.choice(PROXIES)
        request.cookies.update(
            {'spravka':
                 'dD0xNDYwNDQ1NjMwO2k9ODIuMjA4Ljk5LjE5Mzt1PTE0NjA0NDU2MzA2ODM5NzEyNzg7aD0xM2U3ZGY4ZTBmNDdmMmQwZjJiZGJkMDkwMzBjNGRmMA'
             })

        # try:
            # request.meta['proxy'] = "http://%s" % p['ip_port']
            # request.meta['proxy'] = 'http://185.2.32.183:1085'
        # except Exception as e:
        #     logging.error("Exception CustomHttpProxyMiddleware:: %s" % e, _level=logging.CRITICAL)


class CustomUserAgentMiddleware(object):
    """
    Change request headers every time
    """
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)

        request.headers['User-Agent'] = agent
        request.headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        request.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        # print('HEADERS:: |{0}|'.format(request.headers))



