# -*- coding: utf-8 -*-
import scrapy
import datetime
import requests
import json
# from scrapy.selector import Selector
# from subprocess import call




class McaSpider(scrapy.Spider):
    name = 'mca'
    current_year = datetime.date.today().year
    # allowed_domains = ['mca.com']
    # start_urls = ['http://mca.com/']
    def __init__(self):
        self.start_requests()
    def start_requests(self):
        cin_list = requests.request(method='GET', url='http://52.66.198.92/api/mca_info/cinList')
        cin_list = json.loads(cin_list.json())
        # cin_list = ['U74999KA2015PTC103797']
        for cin in cin_list:
            url = 'http://www.mca.gov.in/mcafoportal/vpdDocumentCategoryDetails.do'
            payload = "cinFDetails="+cin+"&companyName=&cartType=&categoryName=ARBE&finacialYear="+str(self.current_year)
            # payload = "cinFDetails="+cin+"&companyName=&cartType=&categoryName=ARBE&finacialYear=2018"
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }
            print(cin)
            yield scrapy.Request(url=url, method='POST', headers=headers, body=payload, callback=self.parse, meta={'cin': cin})
            payload = "cinFDetails="+cin+"&categoryName=OTRE&finacialYear="+str(self.current_year)
            yield scrapy.Request(url=url, method='POST', headers=headers, body=payload, callback=self.parse_eform, meta={'cin': cin})

    def parse(self, response):
        # line = Selector(text=response.strip('\t'))
        res = response.xpath('.//table[@class="result-forms_vpd"]/tr/td/text()').extract()
        print(response.meta['cin'])

        if res:
            url = "http://52.66.198.92/api/mca_info/cinMarked/"
            temp = ''
            for x, y in zip(res[0::2], res[1::2]):
                temp += x.strip() + ' : ' + y.strip() + '<br>'
            # payload = "cinNumer=" + cin + "&doc_present=True"
            payload = "cinNumer="+response.meta['cin']+"&doc_present=True&doc_information="+temp
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }
            requestto = requests.request("POST", url, data=payload, headers=headers)
            print('from true',requestto.text)

        else:
            url = "http://52.66.198.92/api/mca_info/cinMarked/"
            temp = 'no response found today'
            payload = "cinNumer="+response.meta['cin']+"&doc_present=False&doc_information="+temp
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }
            requestto = requests.request("POST", url, data=payload, headers=headers)
            print('from false', requestto)

    def parse_eform(self, response):
        # line = Selector(text=response.strip('\t'))
        res = response.xpath('.//table[@class="result-forms_vpd"]/tr/td/text()').extract()
        print(response.meta['cin'])

        if res:
            url = "http://52.66.198.92/api/mca_info/cinMarked/"
            temp = ''
            for x, y in zip(res[0::2], res[1::2]):
                temp += x.strip() + ' : ' + y.strip() + '<br>'
            # payload = "cinNumer=" + cin + "&doc_present=True"
            payload = "cinNumer="+response.meta['cin']+"&other_eform_documents_present=True&other_eform_documents_information="+temp
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }
            requestto = requests.request("POST", url, data=payload, headers=headers)
            print('from true',requestto.text)

        else:
            url = "http://52.66.198.92/api/mca_info/cinMarked/"
            temp = 'no response found today'
            payload = "cinNumer="+response.meta['cin']+"&other_eform_documents_present=False&other_eform_documents_information="+temp
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }
            requestto = requests.request("POST", url, data=payload, headers=headers)
            print('from false', requestto)