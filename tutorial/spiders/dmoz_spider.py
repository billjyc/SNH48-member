# -*- coding: utf-8 -*-

import sys

from tutorial.helper import Helper

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

    helper = Helper()

    def parse(self, response):
        sel = Selector(response)
        member_links = sel.xpath('//div[@class="member_h zx3"]')
        for member_link in member_links:

            member = MemberItem()
            name = member_link.xpath('./div[@class="mh_w1"]/text()').extract()
            english_name = member_link.xpath('./div[@class="mh_w2"]/text()').extract()
            member['name'] = name[0]
            member['english_name'] = english_name[0]
            member['link'] = member_link.xpath('./div[1]/a/@href').extract()
            strs = member['link'][0].split('=')
            member['id'] = strs[1]

            url = "http://www.snh48.com/" + member['link'][0]
            member['link'] = url
            yield scrapy.Request(url, meta={'item': member}, callback=self.parse_detail)

    def parse_detail(self, response):
        member = response.meta['item']
        sel = Selector(response)

        member['image_link'] = "http://www.snh48.com/" + sel.xpath('//div[@class="mem_p"]/img/@src').extract()[0]

        infos = sel.xpath('//div[@class="mem_w"]/ul')
        member['nick_name'] = infos.xpath('./li[2]/text()').extract()[0]
        member['speciality'] = infos.xpath('./li[4]/text()').extract()[0]
        member['height'] = int(infos.xpath('./li[6]/text()').extract()[0])
        member['hobby'] = infos.xpath('./li[8]/text()').extract()[0]
        member['blood_type'] = infos.xpath('./li[10]/text()').extract()[0]
        member['join_time'] = infos.xpath('./li[12]/text()').extract()[0]
        member['join_time'] = datetime.datetime.strptime(member['join_time'], "%Y-%m-%d").date()

        member['batch'] = infos.xpath('./li[16]/text()').extract()[0]
        member['constellation'] = infos.xpath('./li[18]/text()').extract()[0]
        member['team'] = self.helper.process_item_team(infos.xpath('./li[20]/text()').extract()[0])
        # member['team'] = infos.xpath('./li[20]/text()').extract()[0]
        member['birth_place'] = infos.xpath('./li[22]/text()').extract()[0]
        member['agency'] = infos.xpath('./li[24]/text()').extract()[0]
        member['description'] = infos.xpath('./li[28]/text()').extract()

        # Here we must return the member Item, or the result would not be passed to pipeline
        return member

