from selenium.webdriver.common.keys import Keys
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

print('going to kill all zombie processes of firefox')
ps_result = subprocess.Popen("pkill -f firefox", shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

options = Options()
#options.headless = True
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

print('# creating firefox handler')
browser = webdriver.Firefox(options=options)


username = "mikemx888"
password = "spring60709080"

print('# going to browse the page for first time')

browser.get("https://www.instagram.com/")
#browser.set_window_size(1629, 1025)
#browser.find_element(By.NAME, "username").click()

print("Browse req sent, waiting for loading")
time.sleep(4)
with open('login1.html', 'w') as file_handler:
    file_handler.write(str(browser.page_source))
print("The page content saved to file")

cookie_accept_button = browser.find_element_by_class_name("bIiDR")
cookie_accept_button.click()
print('cookie accept button pressed!')

time.sleep(1)

username_input_field = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
username_input_field.send_keys(username)

print('# username field done')

password_input_field = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.NAME, "password"))
)
password_input_field.send_keys(password)

print('# password field done')


with open('login2.html', 'w') as file_handler:
    file_handler.write(str(browser.page_source))

print('# going to find and click on Log-In')
but = browser.find_element_by_class_name("L3NKy")
but.click()
time.sleep(3)

print("waited after Login pressed, going to continue")

browser.get("https://www.instagram.com/")

time.sleep(2)

with open('login3.html', 'w') as file_handler:
    file_handler.write(str(browser.page_source))


'''
try:
    time.sleep(3)
    but = browser.find_element(By.CSS_SELECTOR, ".sqdOP > .Igw0E").click()
    time.sleep(3)
    print('# first click successful')
except Exception as e:
    print('# first click failed, error: '+str(e))
    # continue

try:
    time.sleep(3)
    but = browser.find_element(By.CSS_SELECTOR, ".sqdOP > .Igw0E").click()
    time.sleep(3)
    print('# second click successful')
except Exception as e:
    print('# second click failed, error: '+str(e))
    # continue
'''