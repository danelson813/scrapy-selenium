# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from shutil import which

class CoinsSpider(scrapy.Spider):
    name = 'coins'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ['https://www.livecoin.net/en']

    def __init__(self):
        options = Options()
        options.add_argument('--headless')

        # gecko_path = which("geckodriver")
        gecko_path = '/Users/geckodriver'

        driver = webdriver.Firefox(executable_path=gecko_path, options=options)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.livecoin.net/en")

        rur_tab = driver.find_elements_by_class_name('filterPanelItem___2z5Gb')
        rur_tab[4].click()

        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        for currency in resp.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'currancy pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get(),
            }
