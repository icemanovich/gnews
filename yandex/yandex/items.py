# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YandexSubject(scrapy.Item):
    title = scrapy.Field()
    title_hash = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()

    rating = scrapy.Field(default=0)
    past_rating = scrapy.Field(default=0)

    vk = scrapy.Field()
    tw = scrapy.Field()
    fb = scrapy.Field()
    ok = scrapy.Field()

    donors_count = scrapy.Field(default=0)
    donors_smi_types = scrapy.Field(default=0)
    views = scrapy.Field(default=0)

    # category_id = scrapy.Field()
    # region_id = scrapy.Field()

    manual = scrapy.Field()

    created_at = scrapy.Field(serializer=str)


class YandexDonor(scrapy.Item):
    title = scrapy.Field()
    subject_id = scrapy.Field()
    category_id = scrapy.Field()
    region_id = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    rating = scrapy.Field()

    vk = scrapy.Field()
    tw = scrapy.Field()
    fb = scrapy.Field()
    ok = scrapy.Field()

    views = scrapy.Field()
    diff = scrapy.Field()
    manual = scrapy.Field()
    link_hash = scrapy.Field()

    smi_id = scrapy.Field()
    smi_tcy = scrapy.Field()
    smi_type = scrapy.Field()

    published_at = scrapy.Field()
    created_at = scrapy.Field(serializer=str)
