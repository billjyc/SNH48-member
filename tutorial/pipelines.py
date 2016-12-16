# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings
from scrapy import log
import chardet
import MySQLdb.cursors
import MySQLdb
import json
import codecs
from jsonencoder import CJsonEncoder

SETTINGS = get_project_settings()


class MemberJsonPipeline(object):
    def __init__(self):
        print 'fuck you!!!!!!'
        self.file = codecs.open('member.json', 'w', encoding='utf-8')
        self.file.write("{\n\"members\": [\n")

    def process_item(self, item, spider):
        print item
        line = json.dumps(dict(item), ensure_ascii=False, cls=CJsonEncoder) + ",\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.write("]\n}")
        self.file.close()


class MySQLStorePipeline(object):
    def __init__(self):
        print 'fuck you too!!'
        dbargs = dict(
            host='127.0.0.1',
            db='snh48',
            user='root',
            passwd='root',
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=True
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.insert_into_table, item)
        return item

    def insert_into_table(self, conn, item):
        #print item
        #print type(item['height']), ' ', type(item['join_time'])
        print len(item['description'])
        split_str = '\n'
        conn.execute("""insert into memberinfo (`id`, `name`, `nick_name`, `height`, `blood_type`, `team`, `batch`, `join_time`, `link`, `image_link`, `hobby`, `description`)
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                     (item['id'], item['name'], item['nick_name'], item['height'], item['blood_type'], item['team'], item['batch'], item['join_time'], item['link'], item['image_link'], item['hobby'], split_str.join(item['description'])))
