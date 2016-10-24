#!/Users/wenjing/.pyenv/shims/python3
#-*- coding:utf-8 -*-

import scrapy
from intern.items import InternItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class SMSpider(scrapy.spiders.CrawlSpider):
    name = "sm"
    base_url = 'http://www.newsmth.net/nForum/board/Intern'
    def __init__(self):
        scrapy.spiders.Spider.__init__(self)
        self.start_urls = [self.base_url]
        self.start_urls.extend([self.base_url+'?p='+str(i) for i in range(2,4)])
      #  print(self.start_urls)
        self.driver = webdriver.PhantomJS()
        self.driver.set_page_load_timeout(15)
        dispatcher.connect(self.spider_closed,signals.spider_closed)


    def spider_closed(self, spider):
        self.driver.quit()


    def parse(self, response):
        print ("parsing:::::::::::::::::::::::::")
        self.driver.get(response.url)
       # print (response.url)
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'table'))
            )
            print ('element:\n', element)
        except Exception as  e:
            print (Exception, ":", e)
           # print ("wait failed")

        page_source = self.driver.page_source
        bs_obj = BeautifulSoup(page_source, "lxml")
       # print (bs_obj)
        table = bs_obj.find('table', class_='board-list tiz')
       # print (table)
        print ("find message =====================\n")
        intern_message = table.find_all('tr')
      #  print (intern_message)
        for message in intern_message:
           # print(message)
            title, href, time, author = '','','',''
            td_9 = message.find('td',class_='title_9')

            if td_9:
                title = td_9.a.get_text()
                href = td_9.a['href']
            td_10 = message.find('td', class_='title_10')
            if td_10:
                time=td_10.get_text()
            td_12 = message.find('td', class_='title_12')
            if td_12:
                author = td_12.get_text()
            item = InternItem()
            print ('title:', title)
            print ('href:', href)
            print ('time:', time)
            print ('author:', author)
            item['title'] = title
            item['href'] = href
            item['time'] = time
            item['author'] = author
            item['base_url_index'] = 0
            root_url = 'http://www.newsmth.net'

            if href !='':
                content = self.parse_content(root_url+href)
                item['content'] = content
                print ('content:',content)


    def parse_content(self,url):
        try:
            self.driver.get(url)
        except Exception as  e:
            print ("give up one detail")
            return ""
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'table')))
            print ('element:\n', element)
        except Exception as e:
            print (Exception, ":", e)
            print ("wait, failed")
        page_source = self.driver.page_source
        bs_obj = BeautifulSoup(page_source, "lxml")
        return bs_obj.find('td', class_='a-content').p.get_text()
