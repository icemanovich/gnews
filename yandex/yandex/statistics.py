import graphitesend
from yandex import settings


class Statistics:

    @staticmethod
    def init():
        return graphitesend.init(
            graphite_server=settings.GRAPHITE_HOST,
            graphite_port=settings.GRAPHITE_PORT,
            system_name='',
            prefix='yanews',
            suffix='.sum'
        )
