# -*- coding: utf-8 -*-

import sys
reload(sys)

sys.setdefaultencoding("utf-8")
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from tutorial.items import MemberItem
from scrapy.spiders import Spider
import scrapy
import datetime


class MemberSpider(Spider):
    name = "snh48"
    allowed_domains = ["snh48.com"]
    start_urls = ["http://www.snh48.com/member_list.php"]

    def parse(self, response):
        sel = Selector(response)
        member_links = sel.xpath('//div[@class="member_h zx3"]')
        for member_link in member_links:
            #print member_link
            member = MemberItem()
            name = member_link.xpath('./div[@class="mh_w1"]/text()').extract()
            # for t in name:
            #     print t.encode("utf-8")
            member['name'] = name[0]
            #print name
            member['link'] = member_link.xpath('./div[1]/a/@href').extract()

            strs = member['link'][0].split('=')
            member['id'] = strs[1]
            #print member['id']
            url = "http://www.snh48.com/" + member['link'][0]
            member['link'] = url
            yield scrapy.Request(url, meta={'item': member}, callback=self.parse_detail)

    def parse_detail(self, response):
        member = response.meta['item']
        sel = Selector(response)

        member['image_link'] = "http://www.snh48.com/" + sel.xpath('//div[@class="mem_p"]/img/@src').extract()[0]
        #print member['image_link'].encode("utf-8")

        infos = sel.xpath('//div[@class="mem_w"]/ul')
        member['nick_name'] = infos.xpath('./li[2]/text()').extract()[0]
        member['height'] = int(infos.xpath('./li[6]/text()').extract()[0])
        member['hobby'] = infos.xpath('./li[8]/text()').extract()[0]
        member['blood_type'] = infos.xpath('./li[10]/text()').extract()[0]
        member['join_time'] = infos.xpath('./li[12]/text()').extract()[0]
        member['join_time'] = datetime.datetime.strptime(member['join_time'], "%Y-%m-%d").date()
        member['batch'] = infos.xpath('./li[16]/text()').extract()[0]
        member['team'] = infos.xpath('./li[20]/text()').extract()[0]
        member['description'] = infos.xpath('./li[28]/text()').extract()
        # print member['join_time'], ' ', member['height']
        # print member
        return member

