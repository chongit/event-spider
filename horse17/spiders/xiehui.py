from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from horse17.items import Horse17Item
from scrapy.http import FormRequest
from scrapy.http import Request
import json
import os

class XiehuiSpider(CrawlSpider):
    name = 'xiehui'
    allowed_domains = ['xiehui.com']
    # start_urls = ['http://www.xiehui.com/searchResult.jsp']

    #rules = (
    #    Rule(SgmlLinkExtractor(allow=r'/searchResult.jsp'), callback='parse_list', follow=True),
    #)
    def start_requests(self):
        '''post request for first page'''
        print 'start request'
        formdata = {"page":'1',"rows":'1'}
        return [FormRequest(url = 
            'http://www.xiehui.com/exhibitPackageView.do?method=searchExhibitPackage',
            formdata = formdata,callback=self.parse_start) ]
    def parse_start(self,response):
        json_object = json.loads(response.body)
        total = json_object['exhibitTotal']
        formdata = {"page":'1',"rows":str(total)}
        return [FormRequest(url = 
            'http://www.xiehui.com/exhibitPackageView.do?method=searchExhibitPackage',
            formdata = formdata,callback=self.parse_list) ]

    def parse_list(self,response):
        json_object = json.loads(response.body)
        for row in json_object['exhibitRows']:
            i = Horse17Item()
            i['starttime'] = row['exhibitStartDate']
            i['endtime'] = row['exhibitEndDate']
            i['title'] = row['exhibitName']
            i['city'] = row['cityDesc']
            i['address'] = row['exhibitLocation']
            i['tags'] = row['keyWord']
            event_id = row['exhibitId']
            url = 'http://www.xiehui.com/events/'+str(event_id)+'/index.html'
            yield Request(url=url, method='get',meta={'item':i}, callback=self.parse_item)
        #return FormRequest(url='',formdata=formdata,callback=self.parse_item)

    def parse_item(self, response):
        sel = Selector(response)
        i = response.meta['item']
        print response.url
        i['logo'] =  sel.xpath('//div[@class="img_logo fl"]/img/@src').extract()[0]
        i['performer'] = sel.xpath('//div[@class="part01-org l"]/p/text()').extract()[0]
        i['organizer'] = ''
        i['organizerlink'] = ''
        timeboth = ''
        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        return i
