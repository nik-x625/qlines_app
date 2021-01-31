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

username = "mikemx888"
password = "spring60709080"

print('# going to browse the page for first time')

browser.get("https://www.instagram.com/")

cookie_button = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".aOOlW")))

with open('login1.html', 'w') as file_handler:
    file_handler.write(str(browser.page_source))

print("# The page content saved to file: login1.html")

cookie_button.click()


#cookie_accept_button = browser.find_element_by_class_name("bIiDR")
# cookie_accept_button.click()
print('# cookie accept button pressed!')


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

print("# The page content saved to file: login2.html")

print('# going to find and click on Log-In')
but = browser.find_element_by_class_name("L3NKy")
but.click()


time.sleep(3)

with open('login3.html', 'w') as file_handler:
    file_handler.write(str(browser.page_source))

print('# click pressed, waiting for not now')
not_now = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sqdOP")))
print('# not now appeared')
not_now.click()

# to click on "Not now" which appears after login
print("# login successful, 'not now' pressed")
time.sleep(0.5)

# it is possible to disable the notification here. Might be needed for a new "click"
tag = 'amsterdam'

print('# all logins went OK, going to browse Tag url: '+str(tag))

browser.get('https://www.instagram.com/explore/tags/'+str(tag))

time.sleep(1)

with open('hashtag_browse.html', 'w') as file_handler:
    file_handler.write(str(browser.page_source))
print("# The page content saved to file: hashtag_browse.html")


# browser.execute_script("window.scrollTo(0,10000)")
#b = browser


links = []

for scroll_times in range(1, 10):    #commented out only for test purposes
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


def trainer(browser, element, url):

    try:
        print('# in trainer function - start - element: '+str(element))
        print('# in trainer function - start - url: '+str(url))

        browser.get(url)
        time.sleep(1)   # todo: enhance this, wait as much as needed, not more
        root = html.fromstring(browser.page_source)
        tree = root.getroottree()
        result = root.xpath('//*[. = "%s"]' % element)
        print('# in trainer function - result: '+str(result))
        res = tree.getpath(result[0])
        print('# res in trainer: '+str(res))
        print('# in trainer function - end')
        return res

    except Exception as e:
        print('# in trainer function, error: '+str(e))
        with open('trainer_error_page_source.html', 'w') as file_handler:
            file_handler.write(str(browser.page_source))

        return None


# training to get the xpath for userid from post page
train_username = 'dream__seekers'
train_url = 'https://www.instagram.com/p/CKcUb-VFxWq/'
userid_learned_xpath = trainer(browser, train_username, train_url)
print('# userid_learned_xpath: '+str(userid_learned_xpath))



# browse the post URL and get the Insta Usernames
insta_id_list = []
for post_link in links: #[0:5]:
    print('')
    print('# going to fetch post page, to get the user ID from it: '+str(post_link))
    browser.get(post_link)

    # with open('post_'+post_link.split('/')[4]+'.html', 'w') as file_handler:
    #    file_handler.write(str(browser.page_source))

    try:

        # To fetch the Username - test purpose, userid is being learned now
        #xpath_without_login = '/html/body/div[1]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a'
        #xpath_with_login_old = "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a"
        #xpath_with_login =     '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/a'

        #insta_id = browser.find_element_by_xpath(userid_learned_xpath).get_attribute('text')
        insta_id = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, str(userid_learned_xpath))))
        insta_id = insta_id.text

        print('# id fetched from post page: '+str(insta_id))
        insta_id_list.append(insta_id)

    except Exception as e:
        print('# in the post page, the insta id not found, error: ' +
              str(e)+'    page link: '+str(post_link))
        continue

print('# all ids found: '+str(insta_id_list))
print('# all ids len: '+str(len(insta_id_list)))


print()
print('browse the users page and fetch the User info, these results will go to DB')


# training to get the xpath for info sections from user page
train_url = 'https://www.instagram.com/nemcy.kz/'

train_posts = '850'
train_followers = '49.6k'
train_following = '385'
train_title = 'NEMCY KAZAKHSTAN'

followers_xpath_trained = trainer(browser, train_followers, train_url)
following_xpath_trained = trainer(browser, train_following, train_url)
title_xpath_trained = trainer(browser, train_title, train_url)
posts_xpath_trained = trainer(browser, train_posts, train_url)


followers_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span'
following_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span'
title_xpath = '/html/body/div[1]/section/main/div/header/section/div[2]/h1'
profile_pic_url_xpath = '/html/body/div[1]/section/main/div/header/div/div/span/img'
description_xpath = '/html/body/div[1]/section/main/div/header/section/div[2]/span'
posts_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span'


print()

print('# followers_xpath:         '+str(followers_xpath))
print('# followers_xpath_trained: '+str(followers_xpath_trained))

print('# following_xpath:         '+str(following_xpath))
print('# following_xpath_trained: '+str(following_xpath_trained))

print('# title_xpath:         '+str(title_xpath))
print('# title_xpath_trained: '+str(title_xpath_trained))

print()


for id in insta_id_list:
    user_doc = {}

    user_url = 'https://www.instagram.com/' + id
    browser.get(user_url)

    print('# fetching username info for: '+str(id))
    followers =         WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, followers_xpath))).text
    following =         WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, following_xpath))).text
    title =             WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, title_xpath))).text
    profile_pic_url =   WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, profile_pic_url_xpath))).text
    description =       WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, description_xpath))).text
    posts =             WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, posts_xpath))).text


    try:


        user_doc['user_id'] = id
        user_doc['followers'] = followers
        user_doc['following'] = following
        user_doc['title'] = title
        user_doc['profile_pic_url'] = profile_pic_url
        user_doc['description'] = description
        user_doc['posts'] = posts

        '''
        print()
        print('# followers count: '+str(followers))
        print('# following count: '+str(following))
        print('# title: '+str(title))
        print('# user pic url: '+str(profile_pic_url))
        print('# description: '+str(description))
        print('# posts: '+str(posts))
        '''
        print()
        print('################# user id: '+str(id))
        print('# user_doc: '+str(user_doc))
        update_profile_in_db({'user_id': id}, user_doc)
        print('# updating the db finished')
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




print('# going to close')
# closing and killing all handlers to save memory
browser.close
browser.quit
ps_result = subprocess.Popen("pkill -f firefox", shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


# u_obj=browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a")
# p_obj.send_keys(Keys.ENTER)
#Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

