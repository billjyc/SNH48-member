# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MemberItem(Item):
    id = Field()
    name = Field()
    height = Field()
    blood_type = Field()
    team = Field()
    batch = Field()
    nick_name = Field()
    join_time = Field()
    batch = Field()
    description = Field()
    link = Field()
    image_link = Field()
    hobby = Field()