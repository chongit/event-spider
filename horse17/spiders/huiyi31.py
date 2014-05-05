# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from horse17.items import Horse17Item
import datetime

class Huiyi31Spider(CrawlSpider):
    name = 'huiyi31'
    allowed_domains = ['31huiyi.com']
    start_urls = ['http://www.31huiyi.com/eventlist/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/eventlist/page/\d+'), follow=True),
        Rule(SgmlLinkExtractor(allow=r'/event/\d+'), callback='parse_item', follow=True),
    )
    def parse_item(self, response):
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
