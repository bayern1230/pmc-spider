# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import FormDataItem
import json
import os

class PmcprojectPipeline:
    def open_spider(self,spider):
        pass

    def process_item(self, item, spider):

        # 将参数写入本地文件
        if type(item) == FormDataItem:

            d = {
                'EntrezSystem2.PEntrez.DbConnector.LastQueryKey':item['lastQueryKey'],
                'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Entrez_Pager.CurrPage':item['currentPage'],
            }

            # 如果没有创建文件则新建文件夹
            if not os.path.exists('settings'):
                os.mkdir('settings')
            # 写入配置文件
            '''特别注意：该文件目录为spider!!!'''
            with open(r'./settings/formSetting.json','w',encoding='utf-8') as f:
                f.write(json.dumps(d))
                print('003')

        return item

    def close_spider(self,spider):
        pass
