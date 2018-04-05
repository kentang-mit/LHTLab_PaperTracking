# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import urlparse
from nips.items import NipsItem
class NipscrawlSpider(scrapy.Spider):
	name = 'nipscrawl'
	allowed_domains = ['papers.nips.cc']
	start_urls = ['https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017']
	crawled = 0
	def parse(self, response):
		self.urls = response.xpath('//a/@href').extract()
		self.urls = filter(lambda x: 'paper' in x, self.urls)
		for url in self.urls:
			print url
			yield Request(url = urlparse.urljoin('https://papers.nips.cc/', url), callback = self.parsedetail)
		

	def parsedetail(self, response):
		url = response.url
		title = response.xpath('//h2[@class="subtitle"]/text()').extract()[0]
		abstract = response.xpath('//p[@class="abstract"]/text()').extract()[0]
		authors = response.xpath('//ul[@class="authors"]/li/a/text()').extract()
		pdf_url = filter(lambda x:'.pdf' in x, response.xpath('//a/@href').extract())[0]
		pdf_url = urlparse.urljoin('https://papers.nips.cc', pdf_url)
		self.crawled += 1
		print self.crawled, len(self.urls)
		item = NipsItem()
		item['url'] = pdf_url
		item['title'] = title
		item['abstract'] = abstract
		item['authors'] = authors
		yield item