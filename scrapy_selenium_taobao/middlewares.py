# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from logging import getLogger
from scrapy.http import HtmlResponse
import time


class SeleniumMiddleware(object):
    def __init__(self):
        self.logger = getLogger(__name__)
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable--gpu')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        # scrap the webpage using headlesschrome
        self.logger.debug('Headlesschrome is starting')
        try:
            self.driver.get(request.url)
            self.driver.find_element_by_xpath('//div[@class="form"]/input').clear()
            self.driver.find_element_by_xpath('//div[@class="form"]/input').send_keys(request.meta['page'])
            self.driver.find_element_by_xpath('//div[@class="form"]/span[@role="button"]').click()
            time.sleep(5)
            return HtmlResponse(url=self.driver.current_url, status=200, body=self.driver.page_source, request=request, encoding='utf-8')
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)
