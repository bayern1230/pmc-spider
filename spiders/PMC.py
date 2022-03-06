import scrapy
from ..items import FormDataItem, TextInfoItem

import json
import os

'''
前端通信协议：
输入参数
-- mode:表示请求的模式，控制进入爬虫后调用的函数
        1:调用term_requests方法，对关键词进行检索
        2:翻页
-- term:模式1时必须传入参数，表示搜索关键词
-- currPage:模式2时必须传入参数，表示搜索页码数
'''


class PmcSpider(scrapy.Spider):
    # API_KEY = '8f7d71639ee4594eb9e5ed799f8712099d08'
    name = 'PMC'
    # allowed_domains = ['https://www.ncbi.nlm.nih.gov/pmc']
    # start_urls = ['https://eutils.ncbi.nlm.nih.gov/entrez/eutils/?db=PMC&id=471697397@qq.com&api_key=8f7d71639ee4594eb9e5ed799f8712099d08']
    # start_urls = ['https://www.ncbi.nlm.nih.gov/pmc/?term=city']

    headers = {
        'authority': 'www.ncbi.nlm.nih.gov',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.ncbi.nlm.nih.gov',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.ncbi.nlm.nih.gov/pmc',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'ncbi_sid=8A1A03E41D9449E1_0312SID; _ga=GA1.2.1761751111.1641628836; _ga=GA1.4.1761751111.1641628836; pmc.article.report=; books.article.report=; _gid=GA1.2.2056390727.1646020357; _gid=GA1.4.2056390727.1646020357; PRESERVTARGET=%2FtYTXpgzJne16bwfb4ZN2lGInyYoZNk58TVbSvhIR0njSJplCp65%2BiF2SZAktvmmznDxgJBJhBCH%0ANoo2je1cMk0RXykLSXa4UwW7u0%2B%2Fc1X7WzHdCi209NjSVDPLNfOmFzmtz50Uuh6EfD95OQ%2BYQ2B%2B%0Aq7BP3es9s8ArLlZd9XW7NS72Ulu8cigULF%2FZADnu%2FPZf8DmPLOXuV6xWf0fqcNlZXwWhiCjrPJiU%0AU594rDm20QBWFe5y0VjWXnJtzYm7uSPkWDQYJ8htbKyWwjn4aG0xcYfTBSBUTOi9A%2Bo1BnUPHLIi%0A8V9%2Fi7S2i2vLCCwVTCSGS0pctKKWZRmzEmP9NB4rA167%2FSMuyX6ezHZNUyztiKaga84g5monl5bT%0AjNlmWeBFQV90piriK2wjmey3mIoTu2eJyDi%2Bx%2FO7pwMTfeiU2WXZ5h3U4kRBxw%2FR6%2FrCMYtVrzXp%0A%2FexiuMJDHQmiDPowP8dxw97tgs353jnBRGe8jpoCPoPG2hywQnwXtxW8SjWp19yTypxVFl4KnD1e%0A5aoPyq%2F7tPDRPbW7UikYuihFvX0mD1TH7A0G9Bk%2B36y%2F7jL8oW7OArzEbESjcx2aVRL%2B3VqzX1Oc%0AZcFWXfVarYgckE8EeyNwFwhPDoASs2T4SVNAJAQ38A0bYzCAxc6mQLqADqesOuuveClDDgB8WITg%0A1QnE32rGsLz37nzAQ89V; NIHSMPROFILE=9i9xFyZxcZ3DeEBWJ1M%2B19DD%2FzbCf8Zw79ClQueW2yaRnXZVzpxdNRD3QoALepAgMsOLgd1tzkv3y7gn4ZIdyIgnGBa4AJUlrrkH%2F%2F8ahbfYoYLcmw9LdqwWZ5l9sqLvU7y9sXa02yjkJeaiVTOOv8isUUAeIcjUWGCJ8vmTNyngQuAj21IjzrVfaD1lIF8tGj4CIgdyBzDQVssnTm6iDAF3km1BY03PMt%2FDZX2g8WJ66ffh2P8z7ZUTvpsbM0cAYtufcVhW0HudnG4JwTUXD13aa05mslsNmE38%2BtTZ%2FUbbGzAt1U8YHP5xZwu6PUzw8O7vlicSTOyBg0X8lArWwmIwn7Z2bJZfA8ZuibwNQIYaxfmJ4q5LibJ2K61iOyLehkqwCbi1qQ5QxLKGphKtqWxxc%2BJ4PNk4sZkqRIqYQlocJp5QP2nwDjVoFSUudbBUYIytT7SAZpMwBeYpZWAqzot2vx7iCggIoxSkAGnBlJXYahZhQruqilnl%2BY4%2BwGc9YkWSQFw9RYzPM8OeZgSqSA%3D%3D; NIHSMSESSION=e8WAZxqAPKeC3n0qfl48og6dr6RdL+sXjqoLnqQSGY26GUCsPHm7mc5Rkzc6aRSg8tm44LtNxGuz6Bhq1Qg52K6Dbol7tUxBlZPX8D/Qc6/Axf/k9qdkNzHy//LNUFNpnkCartGzN1yX4UH/fYbxq6knOoRSGZLCKeOjnY6+umcBgXUPIhcGv+/RRzqxcCGsqjVP3taG+baivEZMIExr0V/pqHHwEc+tcjHWSKgMCl7uzvEyMn+u6FbuPH//nqwl0LRSi1aPEhoxiP8APHIlJzfjK8PNHNq0zPzcuZ+/hdVZgGQfrqQlX3bJBWKRIgcv0GIDFfHs3jFBD4eCQVbeXzNSiv0hUz7pSJ27tU7XVJS2DxIGZEgXUN9JJYdXY80k4XrBmexg3VjJ2kUvdH1cOkBf4V+/UdumBQppgFXxLby3blBwFUM06SXkvpYgWCsklf+0Q4VfnHQZhbkluOkIDsNKnXB+ubf1iIA+K1Kty+HSt/GD8HEBQZA0Y30fjvyag8j/mPkOw/4DjUPzwJnYsuBHAH4Y//gQvO6EHG/ql1eIQaG3rsMguAVRHe3d3mrMyVCrFnuvn90CYH1lRRvoAvf5MsGi63AGaKKZlg8fdLRhpQxLA0j1Pk//ofsLdK8sOiN62PlBkMNgBAvqwTAGBsOIf4wKb1NJ80rVqgzXyO0pi5R1TL/UndotboCTWl7m+kv4A+spHwMbpeT57wQDs7pALXPfskA/7IjK3ul9SfWY7y0YJTB7OAwkCOE1exS2Gy09WneEDUIiRRVQIZLtzu/ljhSj84bqvkdMCKB4Devi66uZwvDUnDBk7a5TklQhgx8rpGJ3Sr+U/Jmm2TgxOKyBNOobc1jk17FB4w4+KwCfv/5DDwjcd/WEOVVkjluHYWSncMs7BsPQhQQV530LMTdyglvRWLLhRhCEK8gOq9b2orvAgl5KcnPOe4+PaNZGKulN/KMQldQSsFqtZCCm+ZMF892TjyJry08W/ZWVZLrThp6lTZcylkVKfenq4y6nPyO1zpy2OwgztPqOakTCbQVbX7THRIb+q/lP4VyvHhEPtUwD18bfx3KTH1yd+W7aXG9FWAA74l15s3KCg7v1hB+IvJMlL4MG0m8RaqqiXBj26tjFWVmhrVU2V3Oj9gkyPbvf+k92aPHldmE8GHBYQacg3vInmLBIc2lQrVrrkhbqVEWUaPymbxV94iq1iGWVig4h+wNBriwA9QtNZUnJECsFNvp14E8B9NP2OzZOcIBC75IY8XB/DALYw5SRnV46dZkG04XJHf00ZD7R2H/gpb52VmR1h+ShfQnt0/qoVbtM5VszPjhIMoqLuCRVxHRphdH0Ha2YYfZQdeZxOuZWua1CED8pZPs7; MyNcbiSigninPreferences=O2dvb2dsZSY%3D; sessionid=eyJzZXR0aW5ncyI6eyJvd25lciI6IjQ3MTY5NzM5N0BxcS5jb20ifX0:1nOXE0:Y0sA7c5eij19XJ5vf2nLIYsRxWjZFZbMcwhcGmErWho; ncbi_prevPHID=CE8CB71521C5ADE10000000000A9002F.m_4; WebCubbyUser=%3Blogged-in%3Dfalse%3Bmy-name%3D%3Bpersistent%3Dfalse%408A1A03E41D9449E1_0312SID; WebEnv=1Jytx5z5rSK9twtFfElhfglnYDGegfLdfnzZekuBMAVA9%408A1A03E41D9449E1_0312SID; _gat_ncbiSg=1; _gat_dap=1; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgBwEECMuAnAMIAsAIgEz4kCsx++ADK2+wEJGtcB0AtnHx0QAGhABjADbIJAawB2UAB4AXTKGaZwAQwDmyBTtXIA9gtEnVUqHB0LUCfVAiiARqdWrT/URPOqUAqqfqZSogDOsEFw/lJiIPja/DqG/sFBIQCiwdAAXgBiphD8CQDMRNplAOwAbFriZFpYdETV2AlkZNrSsooq6o0iWA0gZLXaAGY6UlGd1drVZRONHVhl+ESVjZVYOhImMFCiYM5wMgpyokpqCXTNIIheYBEYAPRvAO7fvAoSbshflJ+L9kIheHpTDA3mB+BIAMR3JJYHKqfIAZQAnhFAvwqLwAAqo/KEgCyJEJcLgACUoBEAK5SVQRAn2KBSXjEqB5OCsvQuQnOO5UbQAOQGAAIAHwgAC+4npCikph0qBu6gwoDKZSmMzm4jK3SwaPpUHKaxA5V2IBqtQ6jQerWwKzGRpAiuVqvVnWGiTuEywZBodwWWCS4lqyMSzHGcvE/n4/HM3s1IBFWEy+XK2lhEk62lQpgkDNK4l9CQDIELxfppZAoceqn48XEFqoo2tqCg00Zg0SUZF4nwOrD+FqRCDCyHbtO/NiiHs/ISY+0MxbiQb01mZqHFq3+rTDzwhFIlBo9EYLHY164PCIAiEInEwYzuW5GFzGGrJYwooA8qKWQJFQ6YgN8ny/P8gJKiCChghCULAdawjLOUR61N0BpRihLplKB2BUJhYwjiAzC8GUdC8KMdAkUw+BEXQbrVCBcqykAA=',
    }

    # 开始运行爬虫时调用该方法--入口
    def start_requests(self):
        # 判断请求模式
        mode = int(getattr(self, 'mode', 0))

        if mode == 1:
            return self.term_requests()
        if mode == 2:
            print("执行mode2")
            return self.changePage()
        if mode == 0:
            raise ValueError("未指定请求方式！")

    # 通过关键词进行检索
    def term_requests(self):
        term = getattr(self, 'term', None)

        # 检测是否传入参数
        if not term:
            print("没有传入关键词参数")
            return

        url = 'https://www.ncbi.nlm.nih.gov/pmc/?term={}'.format(term)

        yield scrapy.Request(
            url=url,
            callback=self.term_parse,
            headers=self.headers,
            meta={'term': term}
        )

    # 执行翻页操作
    def changePage(self):
        url = 'https://www.ncbi.nlm.nih.gov/pmc/'

        # 表单原始数据
        formdata = {
            'term': 'god ',
            'EntrezSystem2.PEntrez.PMC.Pmc_PageController.PreviousPageName': 'results',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.EmailReport': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.EmailFormat': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.EmailCount': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.EmailStart': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.EmailSort': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.Email': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.EmailSubject': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.EmailText': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.EmailQueryKey': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.EmailHID': '18KR4H4UQG0DCPHtUIMRSXtiz0M_HGGHTBC_MYQgYN',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.QueryDescription': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.Key': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.Answer': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.Holding': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.HoldingFft': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.HoldingNdiSet': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.OToolValue': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.EmailTab.SubjectList': '',
            'EntrezSystem2.PEntrez.PMC.Facets.FacetsUrlFrag': 'filters=',
            'EntrezSystem2.PEntrez.PMC.Facets.FacetSubmitted': 'false',
            'EntrezSystem2.PEntrez.PMC.Facets.BMFacets': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sPresentation': 'DocSum',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sPageSize': '20',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sSort': 'none',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FFormat': 'DocSum',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FSort': '',
            'email_format': 'DocSum',
            'email_sort': '',
            'email_count': '20',
            'email_start': '1',
            'email_address': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FileFormat': 'docsum',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.LastPresentation': 'docsum',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.Presentation': 'docsum',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.PageSize': '20',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.LastPageSize': '20',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.Sort': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.LastSort': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FileSort': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.Format': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.LastFormat': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_ResultsSearchController.ResultCount': '1044974',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_ResultsSearchController.RunLastQuery': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Entrez_Pager.cPage': '68',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Entrez_Pager.CurrPage': '69',  # 当前页数
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sPresentation2': 'DocSum',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sPageSize2': '20',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.sSort2': 'none',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FFormat2': 'DocSum',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.FSort2': '',
            'email_format2': 'DocSum',
            'email_sort2': '',
            'email_count2': '20',
            'email_start2': '1',
            'email_address2': '',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_FilterTab.CurrFilter': 'all',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_FilterTab.LastFilter': 'all',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_MultiItemSupl.Pmc_RelatedDataLinks.rdDatabase': 'rddbto',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_MultiItemSupl.Pmc_RelatedDataLinks.DbName': 'pmc',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Discovery_SearchDetails.SearchDetailsTerm': '"god"[All Fields]',
            'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.HistoryDisplay.Cmd': 'PageChanged',
            'EntrezSystem2.PEntrez.DbConnector.Db': 'pmc',
            'EntrezSystem2.PEntrez.DbConnector.LastDb': 'pmc',
            'EntrezSystem2.PEntrez.DbConnector.Term': 'city',
            'EntrezSystem2.PEntrez.DbConnector.LastTabCmd': '',
            'EntrezSystem2.PEntrez.DbConnector.LastQueryKey': '1',  # 重要参数--改变搜索关键字
            'EntrezSystem2.PEntrez.DbConnector.IdsFromResult': '',
            'EntrezSystem2.PEntrez.DbConnector.LastIdsFromResult': '',
            'EntrezSystem2.PEntrez.DbConnector.LinkName': '',
            'EntrezSystem2.PEntrez.DbConnector.LinkReadableName': '',
            'EntrezSystem2.PEntrez.DbConnector.LinkSrcDb': '',
            'EntrezSystem2.PEntrez.DbConnector.Cmd': 'PageChanged',
            'EntrezSystem2.PEntrez.DbConnector.TabCmd': '',
            'EntrezSystem2.PEntrez.DbConnector.QueryKey': '',
            'p$a': 'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Entrez_Pager.Page',
            'p$l': 'EntrezSystem2',
            'p$st': 'pmc',
        }

        # 根据本地文件改变表单数据
        with open('./settings/formSetting.json', encoding='utf-8') as f:
            formSettings = json.loads(f.read())

        formdata.update(formSettings)

        # 判断是否传入自定义参数——页码
        currPage = getattr(self, 'currPage', None)
        if currPage:
            formdata['EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Entrez_Pager.CurrPage'] = currPage
        else:
            raise ValueError("未传入翻页页码!")

        # 提交表单-通过POST方法请求
        yield scrapy.FormRequest(
            url=url,
            headers=self.headers,
            formdata=formdata,
            callback=self.form_parse,
        )

    # 通过关键词查找执行回调函数
    # 功能：设置cookie/表单值，重点更新关键参数
    def term_parse(self, response):
        # 构造表单数据，为翻页做铺垫
        lastQueryKey = response.xpath(
            '''//input[@name="EntrezSystem2.PEntrez.DbConnector.LastQueryKey"]/@value''').extract_first()
        yield FormDataItem(lastQueryKey=lastQueryKey, currentPage='1', term=response.meta['term'])

        print("------------------")
        print("------------------")

        rprt_list = response.xpath('//div[@class="rprt"]')
        for rprt in rprt_list:
            # 标题
            title = ''.join(rprt.xpath('.//div[@class="title"]/a//text()').extract())
            # 链接
            href = rprt.xpath('.//div[@class="title"]/a/@href').extract_first()
            # 作者
            author = ''.join(rprt.xpath('.//div[@class="desc"]//text()').extract())
            # 细节
            details = ''.join(rprt.xpath('.//div[@class="details"]//text()').extract())
            print(title)

            yield TextInfoItem(title=title, href=href,author=author,details=details)
        print("------------------")
        print("------------------")

    # 通过POST请求进行翻页的回调函数
    def form_parse(self, response):

        print("------------------")
        print("------------------")

        rprt_list = response.xpath('//div[@class="rprt"]')
        for rprt in rprt_list:
            # 标题
            title = ''.join(rprt.xpath('.//div[@class="title"]/a//text()').extract())
            # 链接
            href = rprt.xpath('.//div[@class="title"]/a/@href').extract_first()
            # 作者
            author = ''.join(rprt.xpath('.//div[@class="desc"]//text()').extract())
            # 细节
            details = ''.join(rprt.xpath('.//div[@class="details"]//text()').extract())
            print(title)

            yield TextInfoItem(title=title, href=href, author=author, details=details)
        print("------------------")
        print("------------------")
