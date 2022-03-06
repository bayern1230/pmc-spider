# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PmcprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class FormDataItem(scrapy.Item):
    lastQueryKey = scrapy.Field() # 会话参数
    currentPage = scrapy.Field() # 当前页数
