import os
from scrapy import logformatter


class YandexBan(Exception):
    """Yandex return CAPTCHA code"""
    pass


class YandexMockupError(Exception):
    """Yandex page change structure"""
    pass

#
# class PoliteLogFormatter(logformatter.LogFormatter):
#     """ Custom exception for DropItem """
#     def dropped(self, item, exception, response, spider):
#         return {
#             'level': log.DEBUG,
#             # 'format': 'Dropped: {0} {1} {2}'.format(exception, os.linesep, item),
#             'exception': exception,
#             'item': item,
#             'args': response,
#             'msg': 'Dropped: {0} {1}'.format(exception, os.linesep)
#         }
