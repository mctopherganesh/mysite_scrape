# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import Rule, CrawlSpider
from datablogger_scraper.items import DatabloggerScraperItem

class DatabloggerSpider(scrapy.Spider):
    name = 'datablogger'
    allowed_domains = ['www.mctopherganesh.com']
    start_urls = ['http://www.mctopherganesh.com/']
    rules = [
    	Rule(
    		LinkExtractor(
    			canonicalize=True,
    			unique=True
    		),
    		follow=True,
    		callback="parse"
    	)
    ]

    def start_requests(self):
    	for url in self.start_urls:
    		yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        items = []
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        for link in links:
        	is_allowed=False
        	for allowed_domain in self.allowed_domains:
        		if allowed_domain in link.url:
        			is_allowed=True
        	if is_allowed:
        		item = DatabloggerScraperItem()
        		item['url_from'] = response.url
        		item['url_to'] = link.url
        		items.append(item)
        return items
