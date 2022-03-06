# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PmcprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# POST请求方法中的表单数据
class FormDataItem(scrapy.Item):
    term = scrapy.Field() # 搜索关键词
    lastQueryKey = scrapy.Field() # 会话参数
    currentPage = scrapy.Field() # 当前页数

# 文献信息(简略数据)
class TextInfoItem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()
    author = scrapy.Field()
    details = scrapy.Field()