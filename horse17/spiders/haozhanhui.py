from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from horse17.items import Horse17Item
from scrapy.http import Request

class HaozhanhuiSpider(CrawlSpider):
    name = 'haozhanhui'
    allowed_domains = ['haozhanhui.com']
    start_urls = ['http://www.haozhanhui.com/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )
    def start_requests(self):
        '''request seed'''
        return [Request(url='http://www.haozhanhui.com/zhanlanjihua/',
            callback=self.parse_seed)]
    def parse_seed(self,response):
        '''parse seed to get all pages'''
        sel = Selector(response)
        url_list_guonei = sel.xpath('//div[@id="oseexh1"]/ul/li/a/@href').extract()
        url_list_guonei.extend(sel.xpath('//div[@id="oseexh2"]/ul/li/a/@href').extract())
        for index_url in url_list_guonei:
            page_id = index_url[index_url.rfind('_')+1:index_url.rfind('.')]
            desc_url = 'http://www.haozhanhui.com/exhinfo/exhibition_' + page_id+'.html'
            yield  Request(url=desc_url,method='get',
                    callback=self.parse_item) 

    def parse_item(self, response):
        sel = Selector(response)
        i = Horse17Item()
        i['title'] = sel.xpath('//div[@class="exhname"]/h1/text()').extract()[0]
        i['performer'] = ''
        i['logo'] = ''
        i['organizer'] = sel.xpath('//div[@class="exhinfo_center"]/ul/li[3]/a/text()').extract()
        i['organizerlink'] = sel.xpath('//div[@class="exhinfo_center"]/ul/li[3]/a/@href').extract()
        start_end = sel.xpath('//div[@id="exhtime"]/text()').extract()[0]
        i['starttime'] = start_end.split('~')[0]+' '+'09:00:00'
        i['endtime'] = start_end[0:5]+start_end.split('~')[1]+' '+'16:00:00'
        i['description'] = '<br>'.join(sel.xpath('//div[@class="box-bd exhinfo"]/text()').extract())
        i['city'] = '' #TODO
        i['district'] = ''
        i['address'] = ''
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
        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        return i
