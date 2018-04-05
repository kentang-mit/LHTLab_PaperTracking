# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from icml.items import IcmlItem

class IcmlcrawlSpider(scrapy.Spider):
	name = 'icmlcrawl'
	allowed_domains = ['proceedings.mlr.press']
	start_urls = ['http://proceedings.mlr.press/v70/']
	crawled = 0
	
	def parse(self, response):
		self.urls = response.xpath('//p[@class="links"]//a[contains(text(), "abs")]/@href').extract()
		for url in self.urls:
			print url
			yield Request(url = url, callback = self.parsedetail)
	
	def parsedetail(self, response):
		title = response.xpath('//h1/text()').extract()[0]
		abstract = response.xpath('//div[@id="abstract"]/text()').extract()[0].strip()
		pdf_url = response.xpath('//a[contains(text(), "Download PDF")]/@href').extract()[0]
		authors = response.xpath('//div[@id="authors"]/text()').extract()[0].replace('\n','').split(',')
		authors = map(lambda x:x.strip(), authors)
		authors[-1] = authors[-1][:-1][::-1].strip()[::-1]
		self.crawled += 1
		print self.crawled, len(self.urls)
		item = IcmlItem()
		item['url'] = pdf_url
		item['title'] = title
		item['abstract'] = abstract
		item['authors'] = authors
		yield item