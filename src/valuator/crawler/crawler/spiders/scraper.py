# -*- coding: utf-8 -*-
import scrapy
from crawler import scraper_settings


class ScraperSpider(scrapy.Spider):
  name = "scraper"
  
  allowed_domains = [scraper_settings.allowed_domain]
  
  start_urls = [scraper_settings.start_url]

  def parse(self, response):
    for next_page_selector in response.xpath("/html/body/div/div/div/nav/ul/li/a"):
      next_page = next_page_selector.attrib["href"]
      yield response.follow(next_page, callback=self.parse)
      
    for post_selector in response.xpath("/html/body/div/div/div/div/span/a"):
      post = post_selector.attrib["href"]
      yield response.follow(post, callback=self.parse_post)



  def parse_post(self, response):
    author = AuthorLoader(item=Author(), response=response)
    author.add_xpath("born", "/html/body/div/div/p/span[1]/text()")
    author.add_xpath("location", "/html/body/div/div/p/span[2]/text()")
    
    yield author.load_item()
    