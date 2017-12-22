#! -*- coding: utf-8 -*-

import csv
import logging

from selenium import webdriver
from utils import setup_logging

ALCE_URL = 'https://www.al.ce.gov.br/index.php/deputados/nomes-e-historico/'

def init_phantomjs_driver(*args, **kwargs):

    headers = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Connection': 'keep-alive'
    }

    for key, value in headers.items():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

    driver =  webdriver.PhantomJS(*args, **kwargs)
    driver.set_window_size(1400,1000)

    return driver

def run(driver):
    deputies = list()
    article = driver.find_element_by_xpath("//div[@id='articlepxfontsize1']")
    for i in range(1,100):
        try:
            div_aux = article.find_element_by_xpath("div[%d]/div" % (i))
            link = div_aux.find_element_by_xpath("a")
            info = div_aux.text.split('\n')
            deputies.append({'nome': info[0], 'partido': info[1], 'link': link.get_attribute('href')})
        except Exception as e:
            logger.error(e)
            break

    header_keys = list(deputies[0].keys())
    return header_keys, deputies

def persist(header_keys, deputies):
    with open('deputies.csv', 'w+') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=header_keys,quoting=csv.QUOTE_NONNUMERIC,quotechar="'")
        dict_writer.writeheader()
        dict_writer.writerows(deputies)	

def close(driver):
    driver.quit()

if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger(__name__)

    browser = init_phantomjs_driver()
    browser.get(ALCE_URL)

    header_keys, deputies = run(browser)
    persist(header_keys, deputies)

    close(browser)
