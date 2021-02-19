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

from logger_custom import get_module_logger
logger = get_module_logger(__name__)


def kill_zombies():
    print('# going to kill all zombie processes of firefox')
    ps_result = subprocess.Popen("pkill -f firefox", shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


def create_driver():

    options = Options()
    #options.headless = True
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    print('# creating firefox handler')
    browser = webdriver.Firefox(options=options)
    return browser


def login_instagram(browser):
    username = "mikemx888"
    password = "spring60709080"

    print('# going to browse the page for first time')

    try:
        browser.set_page_load_timeout(5)
        browser.get("https://www.instagram.com/")
    except Exception as e:
        print('# in browser.get, login func, error: '+str(e))

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
    not_now = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sqdOP")))
    print('# not now appeared')
    not_now.click()

    # to click on "Not now" which appears after login
    print("# login successful, 'not now' pressed")
    time.sleep(1)


def collect_post_links(browser, tag):
    # it is possible to disable the notification here. Might be needed for a new "click"
    print('# all logins went OK, going to browse Tag url: '+str(tag))

    try:
        browser.set_page_load_timeout(5)
        browser.get('https://www.instagram.com/explore/tags/'+str(tag))
    except Exception as e:
        print('# in browser.get, error: '+str(e))

    time.sleep(1)

    with open('hashtag_browse.html', 'w') as file_handler:
        file_handler.write(str(browser.page_source))
    print("# The page content saved to file: hashtag_browse.html")

    # browser.execute_script("window.scrollTo(0,10000)")
    #b = browser

    links = []

    for scroll_times in range(1, 6):
        counter = 0
        for x in browser.find_elements_by_tag_name('a'):
            link = x.get_attribute('href')
            if 'www.instagram.com/p/' in link and (link not in links):
                counter = counter+1
                links.append(link)
        # print('# all links: '+str(links))
        print('# new added links: '+str(counter))
        print('# all collected links so far: '+str(len(links)))
        browser.execute_script("window.scrollTo(0,2000)")
        time.sleep(1)
        browser.execute_script("window.scrollTo(0,6000)")
        time.sleep(1)
        browser.execute_script("window.scrollTo(0,10000)")
        time.sleep(1)
        browser.execute_script("window.scrollTo(0,15000)")
        time.sleep(1)
        browser.execute_script("window.scrollTo(0,18000)")
        time.sleep(1)
        browser.execute_script("window.scrollTo(0,20000)")
        time.sleep(1)
        browser.execute_script("window.scrollTo(0,25000)")
        time.sleep(1)

    print('# all links collected for this hashtag: '+str(links))
    print('# all links len: '+str(len(links)))
    print()
    return links


def trainer(browser, element, url):

    try:
        print('# in trainer function - start - element: '+str(element))
        print('# in trainer function - start - url: '+str(url))

        try:
            browser.set_page_load_timeout(5)
            browser.get(url)
        except Exception as e:
            print('# in browser.get, trainer, error: '+str(e))

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


def train_the_userid_xpath(train_username, train_url):
    # training to get the xpath for userid from post page
    userid_learned_xpath = trainer(browser, train_username, train_url)
    print('# userid_learned_xpath: '+str(userid_learned_xpath))
    return userid_learned_xpath


def create_id_list(links): #, create_id_list):
    # browse the post URL and get the Insta Usernames
    insta_id_list = []
    for post_link in links:  # [0:5]:
        print('')
        print('# going to fetch post page, to get the user ID from it: '+str(post_link))

        try:
            browser.set_page_load_timeout(5)
            browser.get(post_link)
        except Exception as e:
            print('# in browser.get, in fetching post pages, error: '+str(e))
            print('# sleeping for a while')
            time.sleep(5)

        # with open('post_'+post_link.split('/')[4]+'.html', 'w') as file_handler:
        #    file_handler.write(str(browser.page_source))

        try:
            # To fetch the Username - test purpose, userid is being learned now
            #xpath_without_login = '/html/body/div[1]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a'
            #xpath_with_login_old = "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a"
            #xpath_with_login =     '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/a'

            #insta_id = browser.find_element_by_xpath(userid_learned_xpath).get_attribute('text')
            insta_id = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a"))).text
            
            print('# id fetched from post page: '+str(insta_id))
            insta_id_list.append(insta_id)

        except Exception as e:
            print('# in the post page, the insta id not found, error: ' +
                  str(e)+'    page link: '+str(post_link))
            continue

    print('# all ids found: '+str(insta_id_list))
    print('# all ids len: '+str(len(insta_id_list)))

    print()
    print('going to browse the users page and fetch the User info, these results will go to DB')

    return insta_id_list


def train_user_page_items(browser, training_dict):

    followers_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span'
    following_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span'
    title_xpath = '/html/body/div[1]/section/main/div/header/section/div[2]/h1'
    profile_pic_url_xpath = '/html/body/div[1]/section/main/div/header/div/div/span/img'
    description_xpath = '/html/body/div[1]/section/main/div/header/section/div[2]/span'
    posts_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span'

    followers_xpath_trained = trainer(
        browser, training_dict['train_followers'], training_dict['train_url'])
    following_xpath_trained = trainer(
        browser, training_dict['train_following'], training_dict['train_url'])
    title_xpath_trained = trainer(
        browser, training_dict['train_title'], training_dict['train_url'])
    posts_xpath_trained = trainer(
        browser, training_dict['train_posts'], training_dict['train_url'])

    trained_dict = {'followers_xpath_trained': followers_xpath_trained,
                    'following_xpath_trained': following_xpath_trained,
                    'title_xpath_trained': title_xpath_trained,
                    'profile_pic_url_xpath_trained': profile_pic_url_xpath,
                    'description_xpath_trained': description_xpath,
                    'posts_xpath_trained': posts_xpath_trained,
                    }

    print()

    print('# followers_xpath:         '+str(followers_xpath))
    print('# followers_xpath_trained: ' + str(followers_xpath_trained))

    print('# following_xpath:         '+str(following_xpath))
    print('# following_xpath_trained: ' + str(following_xpath_trained))

    print('# title_xpath:         '+str(title_xpath))
    print('# title_xpath_trained: '+str(title_xpath_trained))
    print()

    return trained_dict


def fetch_user_ids(browser, insta_id_list):  # , trained_dict):
    '''
    followers_xpath = trained_dict['followers_xpath_trained']
    following_xpath = trained_dict['following_xpath_trained']
    title_xpath = trained_dict['title_xpath_trained']
    posts_xpath = trained_dict['posts_xpath_trained']
    profile_pic_url_xpath = trained_dict['profile_pic_url_xpath_trained']
    description_xpath = trained_dict['description_xpath_trained']
    '''

    #followers_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span'
    #following_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span'
    #title_xpath = '/html/body/div[1]/section/main/div/header/section/div[2]/h1'
    profile_pic_url_xpath = '/html/body/div[1]/section/main/div/header/div/div/span/img'
    description_xpath = '/html/body/div[1]/section/main/div/header/section/div[2]/span'
    #posts_xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span'
    website_xpath = '/html/body/div[1]/section/main/div/header/section/div[2]/a'

    for id in insta_id_list:
        user_doc = {}

        user_url = 'https://www.instagram.com/' + id

        try:
            browser.set_page_load_timeout(5)
            browser.get(user_url)

            with open('user.html', 'w') as file_handler:
                file_handler.write(str(browser.page_source))

            print('# fetching username info for: '+str(id))
            print('# fetching followers')
            followers = WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//li/a[text()=" followers"]/span'))).text

            print('# fetching following')
            following = WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//li/a[text()=" following"]/span'))).text

            print('# fetching title')
            #title = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, title_xpath))).text

            title = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".rhpdm"))).text

            print('# title found: '+str(title))

            print('# fetching profile_pic_url')
            profile_pic_url = WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.XPATH, profile_pic_url_xpath))).get_attribute("src")

            print('# fetching description')
            description = WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.XPATH, description_xpath))).text

            print('# fetching posts')
            posts = WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//li/span[text()=" posts"]/span'))).text

            print('# fetching website')
            website = WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.XPATH, website_xpath))).text

        except Exception as e:
            print('# in browser.get, in fetching user id pages, error: '+str(e))
            time.sleep(5)

        try:

            user_doc['user_id'] = id
            user_doc['followers'] = followers
            user_doc['following'] = following
            user_doc['title'] = title
            user_doc['profile_pic_url'] = profile_pic_url
            user_doc['description'] = description
            user_doc['posts'] = posts
            user_doc['website'] = website

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
            time.sleep(5)


def close_browser(browser):

    print('# going to close the browser')
    # closing and killing all handlers to save memory
    browser.close
    browser.quit
    ps_result = subprocess.Popen("pkill -f firefox", shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


if __name__ == '__main__':

    # initial action
    kill_zombies()

    # create the driver
    browser = create_driver()

    # login to instagram
    login_instagram(browser)

    # enter hashtag and collect the post links
    links = collect_post_links(browser, 'california')

    # train the location of th user id in the post page
    #userid_learned_xpath = train_the_userid_xpath('dream__seekers', 'https://www.instagram.com/p/CKcUb-VFxWq/')

    # create list of user IDs
    insta_id_list = create_id_list(links) #, userid_learned_xpath)

    #insta_id_list = ['nemcy.kz', 'ryrapa', '007natalee', 'best_of_sanfrancisco', 'n.lee007', 'benjamin.freemantle', 'dest0n', 'sophiarose92', 'tallyfromthevalley', 'loubelle', 'ccozycomforts', 'radenko_nikolich93', 'pitties_puppy_shop', 'sidonie_el_snake_official', 'heavenscentflowerco', 'shopjenaicollection', 'mywrld.jpg', 'nelsoncanham', 'freebies1075', 'behavioralhealthofca', 'calitrippin', 'therealmaharaj', 'kali_coach', 'dravenghostt', 'bcampbellxxi', 'phukdupnews', 'poshextensionbarhairstore', 'becky_michael_fx',
    #                 'fairysportss', 'dav.al45', 'drtrustenmoore', 'edwin.0498', 'wael.althan', 'gimacompany', 'bmwmgram', 'peaceful.lens', 'maze_of_fez', 'beuty_photo_feya', 'pxl8photography', 'gemstones__hub', 'michellechoates', 'knell____', 'coop_fanpage_', 'canada_ra', 'official.punjatan', 'luise.dottie', 'crimsope_tv', 'allwomenwithcurves', 'lalaily_', 'xmelimel_', 'the.lazer.viking', 'kali_khronicles', 'kaiart89', 'baysushicafe', 'lightingworld', 'sofiabass_art', 'sac_music916', 'craftgraphics.beer']

    # train the the user page items to find the correct location of elements in user page
    '''
    trained_dict = train_user_page_items(browser, {'train_url': 'https://www.instagram.com/nemcy.kz/',
                                                   'train_posts': '854',
                                                   'train_followers': '49.8k',
                                                   'train_following': '386',
                                                   'train_title': 'NEMCY KAZAKHSTAN',
                                                   })
    '''

    # fetch the users from the list and update the DB
    fetch_user_ids(browser, insta_id_list)  # , trained_dict)

    close_browser(browser)
