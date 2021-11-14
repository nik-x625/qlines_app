from selenium.webdriver.common.keys import Keys
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import json
from urllib.request import urlopen
import re
import time
import subprocess
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from mongodb_module import *

import requests
from lxml import html

print('# going to kill all zombie processes of firefox')
ps_result = subprocess.Popen("pkill -f firefox", shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

options = Options()
#options.headless = True
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

print('# creating firefox handler')
browser = webdriver.Firefox(options=options)

print('# going to train')
train_url = 'https://www.instagram.com/nemcy.kz/'

browser.get(train_url)
time.sleep(1)

#res = browser.find_elements_by_xpath("//*[contains(text(), 'seekers.dream')]")

#page = requests.get("https://www.instagram.com/p/CKcUb-VFxWq/")

print('# page source: '+str(browser.page_source))

root = html.fromstring(browser.page_source)
tree = root.getroottree()
result = root.xpath('//*[. = "850"]')

element_xpath = tree.getpath(result[0])

print(element_xpath)

userid = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, str(element_xpath))))

print(str(userid.text))



'''
train_username = 'dream__seekers'
train_url = 'https://www.instagram.com/p/CKcUb-VFxWq/'

browser.get(train_url)
print('# train page loaded I think')
root = html.fromstring(browser.page_source)
tree = root.getroottree()
result_xpath_list = root.xpath('//*[. = "dream__seekers"]' )

userid_xpath = result_xpath_list[0].text
print('# userid_xpath: '+str(userid_xpath))
#res = browser.find_elements_by_xpath("//*[contains(text(), 'My Button')]")
'''


