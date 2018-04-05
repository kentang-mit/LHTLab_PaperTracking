# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import urlparse
from cvpr.items import CvprItem

class CvprcrawlSpider(scrapy.Spider):
	name = 'cvprcrawl'
	allowed_domains = ['openaccess.thecvf.com']
	start_urls = ['http://openaccess.thecvf.com/CVPR2017.py']
	crawled = 0

	def parse(self, response):
		print 1
		self.urls = response.xpath('//dt[@class="ptitle"]/a/@href').extract()
		for url in self.urls:
			yield Request(url = urlparse.urljoin('http://openaccess.thecvf.com/', url), callback = self.parsedetail)
		

	def parsedetail(self, response):
		url = response.url
		pdf_url = urlparse.urljoin(url, response.xpath('//a[contains(text(), "pdf")]/@href').extract()[0])
		title = response.xpath('//div[@id="papertitle"]/text()').extract()[0].strip()
		abstract = response.xpath('//div[@id="abstract"]/text()').extract()[0][1:]
		authors = response.xpath('//div[@id="authors"]//i/text()').extract()
		authors = authors[0].split(', ')
		self.crawled += 1
		print self.crawled, len(self.urls)
		item = CvprItem()
		item['url'] = pdf_url
		item['title'] = title
		item['abstract'] = abstract
		item['authors'] = authors
		yield item



