# -*- coding: utf-8 -*-
import urllib2
import urlparse
import feedparser

import os
import pymysql

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
    

crawled = 0
config = {'conference': '', 'max_results': '100', 'sortBy': 'submittedDate', 'sortOrder':'descending'}
categories_simple = ['cs.cv', 'cs.ai', 'stat.ml', 'cs.lg']
categories = ['cs.cv', 'cs.ai', 'stat.ml', 'cs.lg']
url = 'http://export.arxiv.org/api/query?search_query=cat:'
categories = map(lambda x: url+x, categories)
for i in range(len(categories)):
    for key, value in config.items():
        if key!='conference':
            categories[i] += '&'+key+'='+value
print(categories)

dbObject = dbHandle()
cursor = dbObject.cursor()
for i in range(len(categories)):
    url_ = categories[i]
    cat = categories_simple[i]
    data = urllib2.urlopen(url_).read()
    feed = feedparser.parse(data)
    for entry in feed.entries:
        arxiv_id =  entry.id.split('/abs/')[-1]
        published_time = entry.published
        title = entry.title
        authors = [author.name for author in entry.authors]
        abstract = entry.summary
        links = entry.links
        #year = '20' + arxiv_id[:2]
        #month = str(int(arxiv_id[2:4]))
        year = entry.published.split('-')[-3]
        month = entry.published.split('-')[-2]
        date = entry.published.split('-')[-1][:2]
        conference = 'arXiv'
        for link in links:
            if link['type'] == 'application/pdf':
                pdf_url = link['href']
                break
        for author in authors:
            sql = 'INSERT IGNORE INTO author(name) VALUES (%s)'
            try:
                cursor.execute(sql, author)
                dbObject.commit()
            except:
                print 'INSERTING ERROR at author '+author
        sql = 'INSERT IGNORE INTO article(title, url, abstract, conference, year, month, date) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql,(title, pdf_url, abstract, conference, year, month, date))
            dbObject.commit()
        except Exception as e:
            print e
            print 'INSERTING ERROR at paper '+title
            continue

        sql = 'SELECT id FROM article WHERE title="' + title + '"'
        try:
            cursor.execute(sql)
        except: 
            print 'ERROR when fetching paper ID of ' + title
            continue

        cur_adic = cursor.fetchone()
        try:
            cur_aid = cur_adic[u'id']
        except:
            continue
        for author in authors:
            sql = 'SELECT id FROM author WHERE name="' + author + '"'
            try:
                cursor.execute(sql)
            except:
                try:
                    print 'ERROR when matching author ' + author + ' and paper ' + title
                except:
                    continue
            cur_dic = cursor.fetchone()
            try:
                cur_id = cur_dic[u'id']
            except:
                continue
            sql = 'SELECT * FROM `relationship` WHERE articleid=%s AND authorid=%s'
            try:
                num_of_records = cursor.execute(sql, (cur_aid, cur_id))
            except:
                continue
            if num_of_records > 0:
                continue
            sql = 'INSERT INTO relationship(articleid, authorid) VALUES (%s, %s)'
            try:
                cursor.execute(sql, (cur_aid, cur_id))
                dbObject.commit()
            except:
                print 'ERROR when building relationship between author ' + author + ' and paper ' + title
        print arxiv_id, 'OK!'


        



