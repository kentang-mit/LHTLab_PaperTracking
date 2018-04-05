# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
import pymysql

def dbHandle():
    config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'root',
    'db':'academic',
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor,
    }
    conn = pymysql.connect(**config)
    return conn
    
class MySQLPipeline(object):        
    def process_item(self, item, spider):
        title = item['title']
        authors = item['authors']
        abstract = item['abstract']
        url = item['url']
        conference = 'ICCV'
        year = str(2017)
        month = str(10)
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        for author in authors:
            sql = 'INSERT IGNORE INTO author(name) VALUES (%s)'
            try:
                cursor.execute(sql, author)
                dbObject.commit()
            except:
                print 'INSERTING ERROR at author '+author
        sql = 'INSERT IGNORE INTO article(title, url, abstract, conference, year, month) VALUES (%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql,(title, url, abstract, conference, year, month))
            dbObject.commit()
        except:
            print 'INSERTING ERROR at paper '+title
        
        sql = 'SELECT id FROM article WHERE title="' + title + '"'
        try:
            cursor.execute(sql)
        except: 
            print 'ERROR when fetching paper ID of ' + title
        cur_adic = cursor.fetchone()
        cur_aid = cur_adic[u'id']
        
        for author in authors:
            sql = 'SELECT id FROM author WHERE name="' + author + '"'
            try:
                cursor.execute(sql)
            except:
                print 'ERROR when matching author ' + author + ' and paper ' + title
            cur_dic = cursor.fetchone()
            cur_id = cur_dic[u'id']
            sql = 'INSERT INTO relationship(articleid, authorid) VALUES (%s, %s)'
            try:
                cursor.execute(sql, (cur_aid, cur_id))
                dbObject.commit()
            except:
                print 'ERROR when building relationship between author ' + author + ' and paper ' + title
        return item