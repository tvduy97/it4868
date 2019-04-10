# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from wikipedia.items import WikipediaItem
from collections import Counter  

class PagesSpider(scrapy.Spider):		
    name = 'pages'
    allowed_domains = ['vi.wikipedia.org']
    start_urls = ['http://vi.wikipedia.org/wiki/Kiến_trúc_Đà_Lạt']
    nodes = set()
    
    custom_settings = {
        'DEPTH_LIMIT': 2,
        'DEPTH_PRIORITY': 1 #breadth-first
        # 'DEPTH_PRIORITY': 0 #depth-first
    }

    rules = (
	    Rule(LinkExtractor(allow="https://vi\.wikipedia\.org/wiki/.+_.+",
	                        deny=[
	                            "https://vi\.wikipedia\.org/wiki/Wikipedia.*",
	                            "https://vi\.wikipedia\.org/wiki/Trang_Chính",
	                            "https://vi\.wikipedia\.org/wiki/Thảo_luận.*",
	                            "https://vi\.wikipedia\.org/wiki/Chủ_đề.*",
	                            "https://vi\.wikipedia\.org/wiki/Đặc_biệt.*"
	                            "https://vi\.wikipedia\.org/wiki/Bản_mẫu.*"
	                        ]),
	            callback='parse'),
	)
	
    def parse(self, response):
    	soup = BeautifulSoup(response.body)
    	allLinks = soup.select('p a[href]')
    	for next_page in allLinks:
            if next_page is not None:
                next_page = 'http://vi.wikipedia.org'+next_page['href']
                yield scrapy.Request(next_page, callback=self.parse, dont_filter=False)
                
	    item = WikipediaItem()

	    links = []
	    for link in allLinks:
	    	if link['href'].startswith('/wiki/') and ":" not in link['href']:
	    		links.append(link['title'])
	    cnt = Counter(links)
	    item['links'] = cnt
	    item['title'] = soup.find("h1", {"id": "firstHeading"}).string

        yield item