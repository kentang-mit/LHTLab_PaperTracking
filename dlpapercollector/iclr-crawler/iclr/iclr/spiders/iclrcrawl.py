# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from lxml.html.soupparser import fromstring
import urlparse
from iclr.items import IclrItem
import pickle
'''
#the following lines of code are used to generate url list.
driver = webdriver.PhantomJS()
driver.get('https://openreview.net/group?id=ICLR.cc/2018/Conference')
print(driver.page_source)
tree = fromstring(driver.page_source)
lis = tree.xpath('//h2//a/@href')
lis = filter(lambda x: '/forum' in x, lis)
lis = map(lambda x: urlparse.urljoin('https://openreview.net/', x), lis)
driver.quit()
'''
f = open('urls.pkl','rb')
lis = pickle.load(f)
class IclrcrawlSpider(scrapy.Spider):
    name = 'iclrcrawl'
    #allowed_domains = ['https://openreview.net/group?id=ICLR.cc/2017/conference']
    start_urls = lis
    crawled = 0

    def parse(self, response):
        url = response.url
        pdf_url = urlparse.urljoin('https://openreview.net', response.xpath('//h2//a/@href').extract()[0])
        title = response.xpath('//h2[@class="note_content_title citation_title"]/text()').extract()[0].strip()
        abstract = response.xpath('//span[@class="note-content-value"]/text()')[0].extract()
        authors = response.xpath('//h3/text()').extract()[0]
        authors = authors.split(', ')
        self.crawled += 1
        print self.crawled, url
        item = IclrItem()
        item['url'] = pdf_url
        item['title'] = title
        item['abstract'] = abstract
        item['authors'] = authors
        yield item
