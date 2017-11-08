#! -*- coding: utf-8 -*-

import csv
import logging

from selenium import webdriver
from utils import setup_logging

ALCE_URL = 'https://www.al.ce.gov.br/index.php/deputados/nomes-e-historico/'

def init():
    logger.info("init executed")
    driver = webdriver.PhantomJS()
    driver.get(ALCE_URL)
    return driver

def run(driver):
    deputies = list()
    div = driver.find_element_by_xpath("//div[@id='articlepxfontsize1']")
    for i in range(1,100):
        try:
            div_aux = div.find_element_by_xpath("div[%d]/div" % (i))
            link = div_aux.find_element_by_xpath("a")
            info = div_aux.text.split('\n')
            deputies.append({'nome': info[0], 'partido': info[1], 'link': link.get_attribute('href')})
        except Exception as e:
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
    driver = init()
    header_keys, deputies = run(driver)
    persist(header_keys, deputies)

    close(driver)
