# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from horse17.items import Horse17Item
from scrapy.http import Request
import datetime
import re

class Huiyi31Spider(CrawlSpider):
    name = 'huiyi31'
    allowed_domains = ['31huiyi.com']
    start_urls = ['http://www.31huiyi.com/eventlist/']

    def start_requests(self):
        '''request seed'''
        return [Request(url='http://www.31huiyi.com/eventlist/page/1',
                callback=self.parse_seed)]
    def parse_seed(self,response):
        '''parse seed to get all pages'''
        sel = Selector(response)
        entry = sel.xpath('//div[@class="pager"]/span[1]/text()').extract()[0]
        pagesize = 8
        totalcount = int(re.findall(r"\s(\d+)\s",entry)[0])
        totalpage = totalcount/pagesize
        if totalcount%pagesize>0:
           totalpage = totalpage+1
        for i in range(1,totalpage):
            url = 'http://www.31huiyi.com/eventlist/page/'+str(i)
            yield Request(url=url,method='get',callback=self.parse_list_page)
    def parse_list_page(self,response):
        '''parse list page'''
        sel = Selector(response)
        boxsel = sel.xpath('//dl[@class="list_dl"][1]//dd[not(@class)]')
        for innersel in boxsel:
           i = Horse17Item()
           i['logo'] = innersel.xpath('a/img/@src').extract()[0]
           i['title'] = innersel.xpath('ul/li[1]/a/text()').extract()[0]
           i['source_url'] = innersel.xpath('ul/li[1]/a/@href').extract()[0]
           i['tags'] = innersel.xpath('ul/li[2]/font/text()').extract()[0].strip()
           addressSel = innersel.xpath('ul/li[4]/span/text()').extract()
           if len(addressSel)>0:
               i['address'] =innersel.xpath('ul/li[4]/span/text()').extract()[0].strip()
           else:
               i['address'] = ''
           organizerSel = innersel.xpath('ul/li[5]/a/text()').extract()
           if len(organizerSel)>0:
                i['organizer'] = innersel.xpath('ul/li[5]/a/text()').extract()[0]
                i['organizerlink'] = 'http://www.31huiyi.com'+innersel.xpath('ul/li[5]/a/@href').extract()[0]
           else:
                i['organizer'] = ''
                i['organizerlink'] = ''
           yield Request(url=i['source_url'],method='get',meta={'item':i},callback=self.parse_item)

    def parse_item(self,response):
        sel = Selector(response)
        i = response.meta['item']
        startmonth = sel.xpath('//p[@class="month"]/text()').extract()[0]
        startday = sel.xpath('//p[@class="day"]/text()').extract()[0]
        starttime = sel.xpath('//font[@class="year"]/text()').extract()[0]
        start = startmonth.replace(u'年','-').replace(u'月','-')+startday+' '+starttime+':00'
        enddaytime = sel.xpath('//font[@class="year over"]/text()').extract()[0]
        end = startmonth+' '+enddaytime
        if enddaytime.find(' ')>-1:
            endmonth=enddaytime[0:5]
            endtime = enddaytime[6:11]
            endyear = startmonth[0:4]
            end = endyear+'-'+endmonth.replace('/','-')+' '+endtime+':00'
        i['starttime'] = start
        i['endtime'] = end
        address = sel.xpath('//div[@class="address"]/span//text()').extract()[0].split(' ',1)
        if(len(address) > 1):
            i['city'] = address[0]
        i['performer'] = ''
        txt = sel.xpath('//div[@class="realcontent"]')[0].xpath('p/text()').extract()
        i['description'] = '\n'.join(txt)
        i['district'] = ''
        i['image'] = ''
        i['tel'] = ''
        i['email'] = ''
        i['qq'] = ''
        i['weichat'] = ''
        i['loop'] = ''
        i['groups'] = ''
        i['hot'] = '0'
        return i


    def parse_item111(self, response):
        sel = Selector(response)
        i = Horse17Item()
        i['logo'] = ''
	i['title'] =  sel.xpath('//div[@class=\'eventName\']/h1/text()').extract()[0];
        i['performer'] = ''
#        i['organizer'] = sel.xpath('//div[@class="righttext_title"]/a/text()').extract()[0]
        i['organizer'] = ''
        i['organizerlink'] = ''
        month  = sel.xpath('//p[@class="month"]//text()').extract()[0]
        day = sel.xpath('//p[@class="day"]//text()').extract()[0]
        time = sel.xpath('//font[@class="year"]//text()').extract()[0]
        startDate = (month+day).replace(u'年','-').replace(u'月','-')
        until_time = sel.xpath('//font[@class="year over"]//text()').extract()[0]
        endDate = startDate
        if(until_time.find(' ')>-1):
            splited = until_time.spit(' ',1)
            time = splited[1]
            until = splited[0]
        i['endtime'] = ''
        i['description'] = sel.xpath('//div[@class="realcontent"]/p/text()|//div[class="realcontent"]/h/text()').extract()[0]
        #i['description'] = ''
        address = sel.xpath('//div[@class="address"]/span//text()').extract()[0].split(' ',1)
        if(len(address) == 1):
            i['address'] = address[0]
            i['city'] = ''
        else:
            i['city'] = address[0]
            i['address'] = address[1]
        i['district'] = ''
        i['image'] = ''
        i['tags'] = ''
        i['tel'] = ''
        i['email'] = ''
        i['source_url'] = response.url
        i['qq'] = ''
        i['weichat'] = ''
        i['loop'] = ''
        i['groups'] = ''
        i['hot'] = '0'
        #        i['performer'] = sel.xpath('//div[@class="righttext_title"]/a//text()').extract()[0]
       #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        return i
