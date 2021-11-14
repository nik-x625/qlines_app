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

'''
username = "mikemx888"
password = "spring60709080"

print('# going to browse the page for first time')
browser.get('https://www.instagram.com/')
print('# get done with first browse')

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

with open('the_page_source1_main_page.html', 'w') as file_handler:
    file_handler.write(str(browser.page_source))

print('# going to find and click on Log-In')

# to click the Log In  button
but = browser.find_element_by_class_name("L3NKy")
#but=browser.find_element_by_xpath('//button[text()="Log In"]')
time.sleep(2)
but.click()
time.sleep(1)

try:
    but.click()
except Exception as e:
    print('# exception, second click was not needed, error: '+str(e))
    print('# but it is ok now, continuing')
    continue

time.sleep(2)
print('# Submit sent, waiting to load yes/no page')

print('# page loaded?')
print(str(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "a[href='/explore/']"))))

WebDriverWait(browser, 100).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/explore/']"))
)
print('# yes/no page came! going to sleep a bit')

time.sleep(7)

print('sleep done!')

print('# Login passed, explore href appeared!')

with open('the_page_source2_yesno_page.html', 'w') as file_handler:
    file_handler.write(str(browser.page_source))


# finding and clicking on "yes/no"
but = browser.find_element_by_class_name("yWX7d")
#but=browser.findElement(By.xpath("//button[text()='Log In']"))
time.sleep(2)
but.click()

time.sleep(2)  # better to replace with "wait" using WebDriverWait

with open('the_page_source3_after_login_page.html', 'w') as file_handler:
    file_handler.write(str(browser.page_source))


# asking for hashtag page
print('# going to load hashtag page')
'''

browser.get('https://www.instagram.com/explore/tags/bmw/')

browser.execute_script("window.scrollTo(0,10000)")
b = browser

print('# sleeping after hashtag wget')

time.sleep(5)
with open('the_page_source4_hashtag_result.html', 'w') as file_handler:
    file_handler.write(str(browser.page_source))
print('# hashtag result saved, not sure if good, check the file')

'''
res = browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a")
print('# res: '+str(res))
print('# outerHTML: '+str(res.get_attribute("outerHTML")))
time.sleep(3)
'''

links = []

if 1:  # for scroll_times in range(1, 3):    #commented out only for test purposes
    counter = 0
    for x in browser.find_elements_by_tag_name('a'):
        link = x.get_attribute('href')
        if 'www.instagram.com/p/' in link and (link not in links):
            counter = counter+1
            links.append(link)
    # print('# all links: '+str(links))
    print('# new added links: '+str(counter))
    print('# all collected links so far: '+str(len(links)))
    browser.execute_script("window.scrollTo(0,10000)")
    time.sleep(1)
    browser.execute_script("window.scrollTo(0,10000)")
    time.sleep(1)

print('# all links collected for this hashtag: '+str(links))
print('# all links len: '+str(len(links)))

print()
print()


# browse the post URL and get the Insta Usernames
insta_id_list = []
for post_link in links:
    print('')
    print('# going to fetch post page: '+str(post_link))
    browser.get(post_link)
    try:
        xpath_without_login = '/html/body/div[1]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a'
        xpath_with_login = '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/div/a'

        xpath_for_insta_id = xpath_without_login

        insta_id = b.find_element_by_xpath(
            xpath_for_insta_id).get_attribute('text')
        print('# id fetched from post page: '+str(insta_id))
        insta_id_list.append(insta_id)

    except Exception as e:
        print('# in the post page, the insta id not found, error: ' +
              str(e)+'    page link: '+str(post_link))
        continue

print('# all ids found: '+str(insta_id_list))
print('# all ids len: '+str(len(insta_id_list)))


#insta_id_list = ['webcarbrasil', 'kruttoynuz']
# browse the user's page and fetch the info, this step's result will go to DB in future
print()
for id in insta_id_list:
    user_doc = {}

    user_url = 'https://www.instagram.com/' + id
    browser.get(user_url)
    followers_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span'
    following_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span'
    title_xpath = '/html/body/div[1]/section/main/div/header/section/div[2]/h1'
    profile_pic_xpath = '/html/body/div[1]/section/main/div/header/div/div/span/img'
    description_xpath = '/html/body/div[1]/section/main/div/header/section/div[2]/span'
    try:

        user_doc['user_id'] = id
        followers = browser.find_element_by_xpath(followers_xpath).text
        user_doc['followers'] = followers
        following = browser.find_element_by_xpath(following_xpath).text
        user_doc['following'] = following
        title = browser.find_element_by_xpath(title_xpath).text
        user_doc['title'] = title
        profile_pic_url = browser.find_element_by_xpath(
            profile_pic_xpath).get_attribute('src')
        user_doc['profile_pic_url'] = profile_pic_url

        description = browser.find_element_by_xpath(description_xpath).text
        user_doc['description'] = description

        print()
        print('# user id: '+str(id))
        print('# followers count: '+str(followers))
        print('# following count: '+str(following))
        print('# title: '+str(title))
        print('# user pic url: '+str(profile_pic_url))
        print('# description: '+str(description))
        print('#### updating the db started')
        update_profile_in_db({'user_id': id}, user_doc)
        print('#### updating the db finished')
        print()

    except Exception as e:
        print('# problem in fetching some info from users page: ' +
              str(e)+'  - page id: '+str(id))


# all links = ['https://www.instagram.com/p/CCndSTSJnaG/', 'https://www.instagram.com/p/CCnk7uJqvRV/', 'https://www.instagram.com/p/CCnmSIzBC46/', 'https://www.instagram.com/p/CCnekXcn8Na/', 'https://www.instagram.com/p/CCm9q16hRhq/', 'https://www.instagram.com/p/CCneAf8A-X_/', 'https://www.instagram.com/p/CCnH70pjI79/', 'https://www.instagram.com/p/CCnZ_urjuG8/', 'https://www.instagram.com/p/CCniarBH0iO/', 'https://www.instagram.com/p/CCnvYC9jEna/', 'https://www.instagram.com/p/CCnvROkq7qp/', 'https://www.instagram.com/p/CCnuW3KFpEj/', 'https://www.instagram.com/p/CCnvXn7q2Ms/', 'https://www.instagram.com/p/CCnt4iiIMiu/', 'https://www.instagram.com/p/CCnvW8hjZ41/', 'https://www.instagram.com/p/CCnvW39h-Pw/', 'https://www.instagram.com/p/CCnvWpClE7a/', 'https://www.instagram.com/p/CCnvV2DJh2n/', 'https://www.instagram.com/p/CCnvOI7poqT/', 'https://www.instagram.com/p/CCnvVvjlIFj/', 'https://www.instagram.com/p/CCnvTxPnutJ/', 'https://www.instagram.com/p/CCnvLKFp1p4/', 'https://www.instagram.com/p/CCnvVCmBRLS/', 'https://www.instagram.com/p/CCnvU8Slr5h/', 'https://www.instagram.com/p/CCnvU3mHM8C/', 'https://www.instagram.com/p/CCnvUtgpdsH/', 'https://www.instagram.com/p/CCnvR1SjAUv/', 'https://www.instagram.com/p/CCnvUtYFgdN/', 'https://www.instagram.com/p/CCnvUevFYx2/', 'https://www.instagram.com/p/CCnvQ3uBzmZ/', 'https://www.instagram.com/p/CCnvSVFgtl1/', 'https://www.instagram.com/p/CCnvR27FPpl/', 'https://www.instagram.com/p/CCnvRkaHbC8/', 'https://www.instagram.com/p/CCnvRlnA3rY/', 'https://www.instagram.com/p/CCnvRPbJQf3/', 'https://www.instagram.com/p/CCnvNTyngs3/', 'https://www.instagram.com/p/CCnvRKVBl65/', 'https://www.instagram.com/p/CCnvQxXJ8S0/', 'https://www.instagram.com/p/CCnvOvNo2R5/', 'https://www.instagram.com/p/CCnvEc0pDXO/', 'https://www.instagram.com/p/CCnvObiBBBj/', 'https://www.instagram.com/p/CCnvOW9HoOj/', 'https://www.instagram.com/p/CCnvOEhJVvw/', 'https://www.instagram.com/p/CCnvNWIKa5j/', 'https://www.instagram.com/p/CCnvNBwIyuA/', 'https://www.instagram.com/p/CCnvNEuDL5k/', 'https://www.instagram.com/p/CCnvMecJDI8/', 'https://www.instagram.com/p/CCnvMguhw6B/', 'https://www.instagram.com/p/CCnvMdtHW09/', 'https://www.instagram.com/p/CCnvL7XAsmR/', 'https://www.instagram.com/p/CCnvDzJHUA5/', 'https://www.instagram.com/p/CCnvLTBJI8f/', 'https://www.instagram.com/p/CCnvKFKnGc6/', 'https://www.instagram.com/p/CCnvEaAjJAz/', 'https://www.instagram.com/p/CCnvJibHDhx/', 'https://www.instagram.com/p/CCnvJS_Mqbv/', 'https://www.instagram.com/p/CCnvItrnggc/', 'https://www.instagram.com/p/CCnvIjRjAiM/', 'https://www.instagram.com/p/CCnvIcMi0db/', 'https://www.instagram.com/p/CCnvIZkpBSV/', 'https://www.instagram.com/p/CCnuoS_Fkv_/', 'https://www.instagram.com/p/CCnvG67B0ZG/', 'https://www.instagram.com/p/CCnvFYjpzrT/', 'https://www.instagram.com/p/CCnvFopF_zw/', 'https://www.instagram.com/p/CCnvE5ch5H-/', 'https://www.instagram.com/p/CCnvEwWp40n/', 'https://www.instagram.com/p/CCnu-6eJWIG/', 'https://www.instagram.com/p/CCnuZ-TAdLd/', 'https://www.instagram.com/p/CCntZA3IIpS/', 'https://www.instagram.com/p/CCnvHSPh44N/', 'https://www.instagram.com/p/CCnu424JGHO/', 'https://www.instagram.com/p/CCnvHG3J5o_/', 'https://www.instagram.com/p/CCnvG7gpRaJ/', 'https://www.instagram.com/p/CCnvGe6nVwW/', 'https://www.instagram.com/p/CCnvFmvJH-W/', 'https://www.instagram.com/p/CCnvFPDpmKG/', 'https://www.instagram.com/p/CCnvFOygCnu/', 'https://www.instagram.com/p/CCnvDT2KO_A/', 'https://www.instagram.com/p/CCnupESpe2W/', 'https://www.instagram.com/p/CCnvBkfALj0/', 'https://www.instagram.com/p/CCnvAwPn1l3/', 'https://www.instagram.com/p/CCnu4P7KCEZ/', 'https://www.instagram.com/p/CCnu8TwHKbI/', 'https://www.instagram.com/p/CCnu_qRgob_/', 'https://www.instagram.com/p/CCnu_m_gSd7/', 'https://www.instagram.com/p/CCnu3FkKtzc/', 'https://www.instagram.com/p/CCnu_BvhN0n/', 'https://www.instagram.com/p/CCnu9xWnNHp/', 'https://www.instagram.com/p/CCnukuNjkE2/', 'https://www.instagram.com/p/CCnu91-Jtya/', 'https://www.instagram.com/p/CCnu91rMA4y/', 'https://www.instagram.com/p/CCnu9T3BAjS/', 'https://www.instagram.com/p/CCnux6XJfvw/', 'https://www.instagram.com/p/CCnu85qpP1a/', 'https://www.instagram.com/p/CCnu82spbeM/', 'https://www.instagram.com/p/CCnu83LF5u9/', 'https://www.instagram.com/p/CCnu8BTg2fe/', 'https://www.instagram.com/p/CCnu82jn4ji/', 'https://www.instagram.com/p/CCnu8fEjXL5/', 'https://www.instagram.com/p/CCnu8YKnKxG/', 'https://www.instagram.com/p/CCnu5zujSJk/', 'https://www.instagram.com/p/CCnu8AQiWlp/']
#links_sample = ['https://www.instagram.com/p/CCndSTSJnaG/', 'https://www.instagram.com/p/CCnk7uJqvRV/']
# b=browser
# b.get('https://www.instagram.com/p/CCndSTSJnaG/')

# with open('post_page.html','w+') as f:
#    f.write(b.page_source)

#insta_id = b.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/div/a").get_attribute('text')


'''
links = []
for scroll in range(1,5):
    for x in range(1,6): # rows, count from 1 to 3
        for y in range(1,4): # columns, count from 1 to 5
            path = "/html/body/div[1]/section/main/article/div[%s]/div/div/div[%s]/div[%s]/a" % (scroll, x,y)
            try:
                the_link = browser.find_element_by_xpath(path).get_attribute('href')
                #print(the_link)
                links.append(the_link)
            except Exception as e:
                print('# exception: '+str(e)+'  for x: '+str(x)+'  and y: '+str(y))


print('# all links: '+str(links))
'''


print('# going to close')
# closing and killing all handlers to save memory
browser.close
browser.quit
ps_result = subprocess.Popen("pkill -f firefox", shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


# u_obj=browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a")
# p_obj.send_keys(Keys.ENTER)
#Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


'''
#browser.get('https://www.instagram.com/')  # +username+'/?hl=en')
print('# page source: '+str(browser.page_source))
time.sleep(1)
#bx = browser.find_elements_by_css_selector('input')
emailInput = browser.find_elements_by_css_selector('input')[0]
passwordInput = browser.find_elements_by_css_selector('input')[1]
time.sleep(1)
print('going to fill the forms')
emailInput.send_keys(username)
passwordInput.send_keys(password)
time.sleep(1)
print('going to send enter')
passwordInput.send_keys(Keys.ENTER)
time.sleep(1)
print('Done so far')

#Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# print('# Pagelength: '+str(Pagelength))
#bot = InstagramBot(username, password)
# bot.signIn()
'''

'''
hashtag = 'food'
#browser = webdriver.Chrome('/path/to/chromedriver')
browser.get('https://www.instagram.com/explore/tags/'+hashtag)
Pagelength = browser.execute_script(
    "window.scrollTo(0, document.body.scrollHeight);")

print('# Pagelength: '+str(Pagelength))
'''


'''
class InstagramBot():
    def __init__(self, email, password):
        self.browser = browser
        self.email = username
        self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')

        emailInput = self.browser.find_elements_by_css_selector('form input')[
            0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[
            1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
'''
