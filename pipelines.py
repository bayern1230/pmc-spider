# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import FormDataItem, TextInfoItem
import json
import os
import pymysql


# 默认管道
class PmcprojectPipeline:
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        '''默认管道，分类处理不同项目'''

        '''FormDataItem'''
        # 将参数写入本地文件
        if type(item) == FormDataItem:

            d = {
                'term': item['term'] + ' ',
                'EntrezSystem2.PEntrez.DbConnector.LastQueryKey': item['lastQueryKey'],
                'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Entrez_Pager.CurrPage': item['currentPage'],
            }

            # 如果没有创建文件则新建文件夹
            if not os.path.exists('settings'):
                os.mkdir('settings')

            # 写入配置文件
            '''特别注意：该文件目录为spider!!!'''
            with open(r'./settings/formSetting.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(d))

        '''TextInfoItem'''
        if type(item) == TextInfoItem:
            pass

        return item

    def close_spider(self, spider):
        pass


# 数据库管道
class MysqlPipeline:
    def __init__(self, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings['MYSQL_USER'],
            password=crawler.settings['MYSQL_PASSWORD'],
            port=crawler.settings['MYSQL_PORT'],
            database=crawler.settings['MYSQL_DATABASE'],
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            db=self.database,
        )
        self.cursor = self.db.cursor()

        # 创建表
        sql = '''create table if not exists TextInfoTable(
                 PMCID    varchar(100)    PRIMARY KEY     NOT NULL,
                 title    text                            NOT NULL,
                 author   text                                    ,
                 href     text                                    ,
                 details  text                                        )'''
        self.cursor.execute(sql)

    def process_item(self, item, spider):
        '''Mysql管道'''

        '''FormDataItem'''
        if type(item) == FormDataItem:
            pass

        '''TextInfoItem'''
        if type(item) == TextInfoItem:
            # 插入数据(将Item转为字典)
            itemDict = dict(item)

            # 语句参数
            table = 'TextInfoTable'
            keys = ','.join(itemDict.keys())
            values = ','.join(["'%s'" % i for i in itemDict.values()])

            # 插入语句
            sql = '''insert ignore into {table} ({keys})
                     values
                     ({values})'''.format(table=table, keys=keys, values=values)

            # 执行插入语句并判断数据是否已经存在
            if self.cursor.execute(sql):
                print("插入数据成功")
                self.db.commit()
            else:
                print("数据库中已经存有该数据！")

        return item

    def close_spider(self, spider):
        self.db.close()
