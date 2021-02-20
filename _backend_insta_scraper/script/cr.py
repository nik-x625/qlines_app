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
import configparser
import psutil

from logger_custom import get_module_logger
logger = get_module_logger(__name__)


def manual_sleep():
    configParser = configparser.RawConfigParser()
    configParser.read('./manual_actions.cfg')
    res = configParser.get('section1', 'manual_sleep')
    res = int(res)
    return res

def flow_is_ok():
    if psutil.cpu_times_percent().iowait > 10:
        print('# in flow_is_ok, wait io is high!!!')
        return 0
    
    if psutil.cpu_percent() > 60:
        print('# in flow_is_ok, cpu percentage is high!!!')
        return 0

    print('# in flow_is_ok, so far so good')
    
    return 1


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

def create_driver_chrome():

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(executable_path='/opt/source/_backend_insta_scraper/script/chromedriver', options=options)

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

    #with open('login1.html', 'w') as file_handler:
    #    file_handler.write(str(browser.page_source))

    #print("# The page content saved to file: login1.html")

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

    #with open('login2.html', 'w') as file_handler:
    #    file_handler.write(str(browser.page_source))
    #print("# The page content saved to file: login2.html")

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
    print('# going to browse Tag url: '+str(tag))

    try:
        #browser.set_page_load_timeout(5)
        browser.get('https://www.instagram.com/explore/tags/'+str(tag))
    except Exception as e:
        print('# in func collect_post_links, in step browser.get, error: '+str(e))

    time.sleep(3)

    #with open('hashtag_browse.html', 'w') as file_handler:
    #    file_handler.write(str(browser.page_source))
    #print("# The page content saved to file: hashtag_browse.html")

    # browser.execute_script("window.scrollTo(0,10000)")
    #b = browser

    links = []

    for iter in range(2, 6):  # for scroll_times in range(1, 6):
        counter = 0

        browser.execute_script("window.scrollTo(0,%d)" %(iter*1000))
        time.sleep(1)

        for x in browser.find_elements_by_tag_name('a'):
            link = ''
            try:
                link = x.get_attribute('href')
            except Exception as e:
                print('# in collect_post_links, in x.get_attribute, error: '+str(e))
            if 'www.instagram.com/p/' in link and (link not in links):
                counter = counter+1
                links.append(link)

        print('# in iteration, new added links: '+str(counter))
        print('# in iteration, all collected links so far: '+str(len(links)))


    print('# the target tag was: '+str(tag))
    print('# all links collected for this hashtag: '+str(links))
    print('# all links len: '+str(len(links)))
    print('')
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


def create_id_list(links, browser):  # , create_id_list):
    # browse the post URL and get the Insta Usernames
    insta_id_list = []

    failed_wget = 0

    for post_link in links[0:7]:  # [0:5]:
        print('')
        print('# going to fetch post page, to get the user ID from it: '+str(post_link))

        try:
            
            browser.set_page_load_timeout(5)
            #browser.implicitly_wait(5);
            print('# setting set_page_load_timeout done')

            if not flow_is_ok() or failed_wget > 2 or manual_sleep():#read_config('do_sleep'):
                
                print('# flow control triggered, flow_is_ok: '+str(flow_is_ok()))
                print('# flow control triggered, failed_wget: '+str(failed_wget))
                browser.close()
                kill_zombies()
                failed_wget = 0

                while not flow_is_ok():
                    print('# sleeping a bit.......................')
                    time.sleep(1)
                while manual_sleep():
                    print('# sleeping a bit.......................manually requested')
                    time.sleep(1)

                print('# !!!!!!!!!!!!!!! Restarting the handler...')
                browser = create_driver()
                #login_instagram(browser)



            print("# going to do the GET")

            browser.get(post_link)
            print('# page get finished')
        except Exception as e:
            print('# in browser.get, in fetching post pages, error: '+str(e))
            if 'Timeout loading page after' in str(e):
                failed_wget = failed_wget + 1
                print('# failure added, failed_wget count is: '+str(failed_wget))
            time.sleep(3)

        #with open('post_'+post_link.split('/')[4]+'.html', 'w') as file_handler:
        #    file_handler.write(str(browser.page_source))

        try:
            # To fetch the Username - test purpose, userid is being learned now
            #xpath_without_login = '/html/body/div[1]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a'
            #xpath_with_login_old = "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a"
            #xpath_with_login =     '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/a'
            xpath_without_login  = '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/a'
            xpath_with_login = "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a"

            xpath_for_username = xpath_without_login

            print("# going to read the userid")

            insta_id = browser.find_element_by_xpath(xpath_for_username).get_attribute('text')

            #insta_id = WebDriverWait(browser, 5).until(
            #    EC.presence_of_element_located((By.XPATH, xpath_with_login))).text

            print('################# id fetched from post page: '+str(insta_id))
            insta_id_list.append(insta_id)

            #browser.close()

        except Exception as e:
            print('# in the post page, the insta id not found, error: ' + str(e)+'  page link: '+str(post_link))
            continue

    print('# all ids found: '+str(insta_id_list))
    print('# all ids len: '+str(len(insta_id_list)))

    print()
    print('# finished in func create_id_list, probably going to fetch user info')

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
    print('# in func fetch_user_ids')
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
        followers = ''
        following = ''
        title = ''
        description = ''
        profile_pic_url = ''
        posts = ''
        website = ''


        print('# fetching user info for: '+str(id))

        user_url = 'https://www.instagram.com/' + id


        if not flow_is_ok() or manual_sleep():#read_config('do_sleep'):
            
            print('# flow control triggered, flow_is_ok: '+str(flow_is_ok()))
            browser.close()
            kill_zombies()
            failed_wget = 0

            while not flow_is_ok():
                print('# sleeping a bit.......................')
                time.sleep(1)
            while manual_sleep():
                print('# sleeping a bit.......................manually requested')
                time.sleep(1)

            print('# !!!!!!!!!!!!!!! Restarting the handler...')
            browser = create_driver()
            #login_instagram(browser)



        try:
            print('# going to call wget')
            #browser.set_page_load_timeout(5)
            browser.get(user_url)
            print('# calling wget passed')

            #with open('user.html', 'w') as file_handler:
            #    file_handler.write(str(browser.page_source))

            print('# fetching user info for: '+str(id))

            followers = WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//li/a[text()=" followers"]/span'))).text
            print('# followers: '+str(followers))


            following = WebDriverWait(browser, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//li/a[text()=" following"]/span'))).text
            print('# following: '+str(following))

            #print('# fetching title')
            #title = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, title_xpath))).text
            title = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".rhpdm"))).text
            print('# title: '+str(title))


            print('# fetching profile_pic_url')
            profile_pic_url = WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.XPATH, profile_pic_url_xpath))).get_attribute("src")
            print('# profile_pic_url: '+str(profile_pic_url))

            print('# fetching description')
            description = WebDriverWait(browser, 3).until(
                EC.presence_of_element_located((By.XPATH, description_xpath))).text
            print('# description: '+str(description))

            #print('# fetching posts')
            #posts = WebDriverWait(browser, 3).until(EC.presence_of_element_located(
            #    (By.XPATH, '//li/span[text()=" posts"]/span'))).text

            #print('# fetching website')
            #website = WebDriverWait(browser, 3).until(
            #    EC.presence_of_element_located((By.XPATH, website_xpath))).text

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
            #user_doc['posts'] = posts
            #user_doc['website'] = website

            '''
            print()
            print('# followers count: '+str(followers))
            print('# following count: '+str(following))
            print('# title: '+str(title))
            print('# user pic url: '+str(profile_pic_url))
            print('# description: '+str(description))
            print('# posts: '+str(posts))
            '''

            print('# user id: '+str(id))
            print('# user_doc: '+str(user_doc))
            update_profile_in_db({'user_id': id}, user_doc)
            print('################# updating the db finished')
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



def prepared_post_list():
    list_of_posts = ['https://www.instagram.com/p/CLevqFlrKEO/', 'https://www.instagram.com/p/CLevRt8DoPu/', 'https://www.instagram.com/p/CLeX7EAss4b/', 'https://www.instagram.com/p/CLeysg0DBg-/', 'https://www.instagram.com/p/CLezyCJju39/', 'https://www.instagram.com/p/CLeZB6MHDeu/', 'https://www.instagram.com/p/CLdjw1fApfU/', 'https://www.instagram.com/p/CLeT_IopoYw/', 'https://www.instagram.com/p/CLeHek6jWka/', 'https://www.instagram.com/p/CLe6UeJgDct/', 'https://www.instagram.com/p/CLe6Uc2hmiU/', 'https://www.instagram.com/p/CLe6UOiFnv3/', 'https://www.instagram.com/p/CLe6T1AnbDe/', 'https://www.instagram.com/p/CLe6IO4nJXo/', 'https://www.instagram.com/p/CLe6TkgBNl6/', 'https://www.instagram.com/p/CLe6S0JnVZT/', 'https://www.instagram.com/p/CLe6SzzFbLR/', 'https://www.instagram.com/p/CLe6StQjbH9/', 'https://www.instagram.com/p/CLe6SvPlokk/', 'https://www.instagram.com/p/CLe6SMorLOJ/', 'https://www.instagram.com/p/CLe6R4aBbgN/', 'https://www.instagram.com/p/CLe6R3hHFYN/', 'https://www.instagram.com/p/CLe6Rv5gCt6/', 'https://www.instagram.com/p/CLe6RcpnSYk/', 'https://www.instagram.com/p/CLe6RR2D6mP/', 'https://www.instagram.com/p/CLe6QzDBok7/', 'https://www.instagram.com/p/CLe6Qc6AWG6/', 'https://www.instagram.com/p/CLe6QK_htjV/', 'https://www.instagram.com/p/CLe6PSgBUbZ/', 'https://www.instagram.com/p/CLe6O51FFhe/', 'https://www.instagram.com/p/CLe6N9qAhRr/', 'https://www.instagram.com/p/CLe6NI-sUvh/', 'https://www.instagram.com/p/CLe6NCShP-6/', 'https://www.instagram.com/p/CLe6GjZnraz/', 'https://www.instagram.com/p/CLe6GbsB3Sp/', 'https://www.instagram.com/p/CLe6GaPhQLw/', 'https://www.instagram.com/p/CLe6CXBhz9s/', 'https://www.instagram.com/p/CLe6GAYHOoc/', 'https://www.instagram.com/p/CLe6F_nAkCF/', 'https://www.instagram.com/p/CLe6GCrlvOE/', 'https://www.instagram.com/p/CLe6F5kA7tR/', 'https://www.instagram.com/p/CLe6FYblzW1/', 'https://www.instagram.com/p/CLe6E0Enu3A/', 'https://www.instagram.com/p/CLe6EYwszym/', 'https://www.instagram.com/p/CLe6EMuHt9f/', 'https://www.instagram.com/p/CLe5454D-Ak/', 'https://www.instagram.com/p/CLe5x2ZFU4Z/', 'https://www.instagram.com/p/CLe5p96HNl-/', 'https://www.instagram.com/p/CLe5npBnlqH/', 'https://www.instagram.com/p/CLe5kehBcDn/', 'https://www.instagram.com/p/CLe5idRBvl1/', 'https://www.instagram.com/p/CLevl3sgUs0/', 'https://www.instagram.com/p/CLevWyuh5KJ/', 'https://www.instagram.com/p/CLeuWAxhe5H/', 'https://www.instagram.com/p/CLd7nWrHYnM/', 'https://www.instagram.com/p/CLdgtfqhicX/', 'https://www.instagram.com/p/CLdbc4Rn0I4/', 'https://www.instagram.com/p/CLcqwNrn1-Q/', 'https://www.instagram.com/p/CLcZCorlybZ/', 'https://www.instagram.com/p/CLcMQnal_I1/', 'https://www.instagram.com/p/CLahN7_n0Am/', 'https://www.instagram.com/p/CLaZVr1HYRx/', 'https://www.instagram.com/p/CHy2Wxig92V/', 'https://www.instagram.com/p/CLe6CcAHY7G/', 'https://www.instagram.com/p/CLe6CYenkav/', 'https://www.instagram.com/p/CLe6B7PLaeF/', 'https://www.instagram.com/p/CLe6B8MjEKN/', 'https://www.instagram.com/p/CLe5wioAjVQ/', 'https://www.instagram.com/p/CLe6BnwBjA-/', 'https://www.instagram.com/p/CLe6BzwB5Uw/', 'https://www.instagram.com/p/CLe6BvDsuDx/', 'https://www.instagram.com/p/CLe6BtiH2Yz/', 'https://www.instagram.com/p/CLe6AXNHxhf/', 'https://www.instagram.com/p/CLe6BG9ppaR/', 'https://www.instagram.com/p/CLe6Auul_aC/', 'https://www.instagram.com/p/CLe6AgppKUw/', 'https://www.instagram.com/p/CLe6AMsAht0/', 'https://www.instagram.com/p/CLe6AB0rtHe/', 'https://www.instagram.com/p/CLe5_52pMSJ/', 'https://www.instagram.com/p/CLe570bJEbY/', 'https://www.instagram.com/p/CLe500hFGKn/',
                     'https://www.instagram.com/p/CLevqFlrKEO/', 'https://www.instagram.com/p/CLevRt8DoPu/', 'https://www.instagram.com/p/CLeX7EAss4b/', 'https://www.instagram.com/p/CLeysg0DBg-/', 'https://www.instagram.com/p/CLezyCJju39/', 'https://www.instagram.com/p/CLeZB6MHDeu/', 'https://www.instagram.com/p/CLdjw1fApfU/', 'https://www.instagram.com/p/CLeT_IopoYw/', 'https://www.instagram.com/p/CLeHek6jWka/', 'https://www.instagram.com/p/CLe6UeJgDct/', 'https://www.instagram.com/p/CLe6Uc2hmiU/', 'https://www.instagram.com/p/CLe6UOiFnv3/', 'https://www.instagram.com/p/CLe6T1AnbDe/', 'https://www.instagram.com/p/CLe6IO4nJXo/', 'https://www.instagram.com/p/CLe6TkgBNl6/', 'https://www.instagram.com/p/CLe6S0JnVZT/', 'https://www.instagram.com/p/CLe6SzzFbLR/', 'https://www.instagram.com/p/CLe6StQjbH9/', 'https://www.instagram.com/p/CLe6SvPlokk/', 'https://www.instagram.com/p/CLe6SMorLOJ/', 'https://www.instagram.com/p/CLe6R4aBbgN/', 'https://www.instagram.com/p/CLe6R3hHFYN/', 'https://www.instagram.com/p/CLe6Rv5gCt6/', 'https://www.instagram.com/p/CLe6RcpnSYk/', 'https://www.instagram.com/p/CLe6RR2D6mP/', 'https://www.instagram.com/p/CLe6QzDBok7/', 'https://www.instagram.com/p/CLe6Qc6AWG6/', 'https://www.instagram.com/p/CLe6QK_htjV/', 'https://www.instagram.com/p/CLe6PSgBUbZ/', 'https://www.instagram.com/p/CLe6O51FFhe/', 'https://www.instagram.com/p/CLe6N9qAhRr/', 'https://www.instagram.com/p/CLe6NI-sUvh/', 'https://www.instagram.com/p/CLe6NCShP-6/', 'https://www.instagram.com/p/CLe6GjZnraz/', 'https://www.instagram.com/p/CLe6GbsB3Sp/', 'https://www.instagram.com/p/CLe6GaPhQLw/', 'https://www.instagram.com/p/CLe6CXBhz9s/', 'https://www.instagram.com/p/CLe6GAYHOoc/', 'https://www.instagram.com/p/CLe6F_nAkCF/', 'https://www.instagram.com/p/CLe6GCrlvOE/', 'https://www.instagram.com/p/CLe6F5kA7tR/', 'https://www.instagram.com/p/CLe6FYblzW1/', 'https://www.instagram.com/p/CLe6E0Enu3A/', 'https://www.instagram.com/p/CLe6EYwszym/', 'https://www.instagram.com/p/CLe6EMuHt9f/', 'https://www.instagram.com/p/CLe5454D-Ak/', 'https://www.instagram.com/p/CLe5x2ZFU4Z/', 'https://www.instagram.com/p/CLe5p96HNl-/', 'https://www.instagram.com/p/CLe5npBnlqH/', 'https://www.instagram.com/p/CLe5kehBcDn/', 'https://www.instagram.com/p/CLe5idRBvl1/', 'https://www.instagram.com/p/CLevl3sgUs0/', 'https://www.instagram.com/p/CLevWyuh5KJ/', 'https://www.instagram.com/p/CLeuWAxhe5H/', 'https://www.instagram.com/p/CLd7nWrHYnM/', 'https://www.instagram.com/p/CLdgtfqhicX/', 'https://www.instagram.com/p/CLdbc4Rn0I4/', 'https://www.instagram.com/p/CLcqwNrn1-Q/', 'https://www.instagram.com/p/CLcZCorlybZ/', 'https://www.instagram.com/p/CLcMQnal_I1/', 'https://www.instagram.com/p/CLahN7_n0Am/', 'https://www.instagram.com/p/CLaZVr1HYRx/', 'https://www.instagram.com/p/CHy2Wxig92V/', 'https://www.instagram.com/p/CLe6CcAHY7G/', 'https://www.instagram.com/p/CLe6CYenkav/', 'https://www.instagram.com/p/CLe6B7PLaeF/', 'https://www.instagram.com/p/CLe6B8MjEKN/', 'https://www.instagram.com/p/CLe5wioAjVQ/', 'https://www.instagram.com/p/CLe6BnwBjA-/', 'https://www.instagram.com/p/CLe6BzwB5Uw/', 'https://www.instagram.com/p/CLe6BvDsuDx/', 'https://www.instagram.com/p/CLe6BtiH2Yz/', 'https://www.instagram.com/p/CLe6AXNHxhf/', 'https://www.instagram.com/p/CLe6BG9ppaR/', 'https://www.instagram.com/p/CLe6Auul_aC/', 'https://www.instagram.com/p/CLe6AgppKUw/', 'https://www.instagram.com/p/CLe6AMsAht0/', 'https://www.instagram.com/p/CLe6AB0rtHe/', 'https://www.instagram.com/p/CLe5_52pMSJ/', 'https://www.instagram.com/p/CLe570bJEbY/', 'https://www.instagram.com/p/CLe500hFGKn/',
                     'https://www.instagram.com/p/CLe5yDZl1do/', 'https://www.instagram.com/p/CLe5JOigLQD/', 'https://www.instagram.com/p/CLe3m35JChq/', 'https://www.instagram.com/p/CLK_KD8Hr30/', 'https://www.instagram.com/p/CIKiXlIgbU5/', 'https://www.instagram.com/p/CIBWb2bASnb/', 'https://www.instagram.com/p/CLe5-SGJEpI/', 'https://www.instagram.com/p/CLe593kBxN1/', 'https://www.instagram.com/p/CLe59tQncTD/', 'https://www.instagram.com/p/CLe59qUjXmb/', 'https://www.instagram.com/p/CLe59cDBMOB/', 'https://www.instagram.com/p/CLe572XADFx/', 'https://www.instagram.com/p/CLe57R0JUV0/', 'https://www.instagram.com/p/CLe57lGsROq/', 'https://www.instagram.com/p/CLe57p6sMm4/', 'https://www.instagram.com/p/CLe57jalapP/', 'https://www.instagram.com/p/CLe57jdnpJe/', 'https://www.instagram.com/p/CLe57A7APHX/', 'https://www.instagram.com/p/CLe56xkh-Nu/', 'https://www.instagram.com/p/CLe56tfFAwp/', 'https://www.instagram.com/p/CLe56b2Mttx/', 'https://www.instagram.com/p/CLe56P1hrzS/', 'https://www.instagram.com/p/CLe56HoMtq9/', 'https://www.instagram.com/p/CLe554ODuFN/', 'https://www.instagram.com/p/CLe55hHlf2I/', 'https://www.instagram.com/p/CLe55aRJhOF/', 'https://www.instagram.com/p/CLe5y-hFmyP/', 'https://www.instagram.com/p/CLe55M3rZQn/', 'https://www.instagram.com/p/CLe55N0p9PQ/', 'https://www.instagram.com/p/CLe55LIJCOL/', 'https://www.instagram.com/p/CLe55BMBh1B/', 'https://www.instagram.com/p/CLe54hABdQt/', 'https://www.instagram.com/p/CLe54c2ptSJ/', 'https://www.instagram.com/p/CLe5zazgfLF/', 'https://www.instagram.com/p/CLe5uERhaum/', 'https://www.instagram.com/p/CLe39K8ByMu/', 'https://www.instagram.com/p/CLdb8pzhaxU/', 'https://www.instagram.com/p/CLe54ayHf0L/', 'https://www.instagram.com/p/CLe53ygJoOd/', 'https://www.instagram.com/p/CLe54FdjeBG/', 'https://www.instagram.com/p/CLe54ABBSuI/', 'https://www.instagram.com/p/CLe5312BYCy/', 'https://www.instagram.com/p/CLe53b5hD-3/', 'https://www.instagram.com/p/CLe52yPBeqV/', 'https://www.instagram.com/p/CLe52i6sn_R/', 'https://www.instagram.com/p/CLe52YqB2h7/', 'https://www.instagram.com/p/CLe51Y7LlNK/', 'https://www.instagram.com/p/CLe51CPnCst/', 'https://www.instagram.com/p/CLe501WDkow/', 'https://www.instagram.com/p/CLe500op7AA/', 'https://www.instagram.com/p/CLe5z5xHRms/', 'https://www.instagram.com/p/CLe5zj-lF79/', 'https://www.instagram.com/p/CLe5vB6p2xF/', 'https://www.instagram.com/p/CLe5uM6pZ_r/', 'https://www.instagram.com/p/CLe5ti9FMpU/', 'https://www.instagram.com/p/CLe5YEcFcFs/', 'https://www.instagram.com/p/CLe5GqjgrKB/', 'https://www.instagram.com/p/CLe1c3XARPP/', 'https://www.instagram.com/p/CLdb7KuBpqZ/', 'https://www.instagram.com/p/CLSdSnpnCTb/', 'https://www.instagram.com/p/CLe5zAKHLxn/', 'https://www.instagram.com/p/CLe5y9rnx45/', 'https://www.instagram.com/p/CLe5uYnBhr2/', 'https://www.instagram.com/p/CLe5yDRHGAH/', 'https://www.instagram.com/p/CLe5xbcJ9pr/', 'https://www.instagram.com/p/CLe5xcUp1S9/', 'https://www.instagram.com/p/CLe5xN6HEem/', 'https://www.instagram.com/p/CLe5w8pD_5o/', 'https://www.instagram.com/p/CLe5wvyhFsy/', 'https://www.instagram.com/p/CLe5wkVpRQO/', 'https://www.instagram.com/p/CLe5v56DFZ2/', 'https://www.instagram.com/p/CLe5v0wjR5r/', 'https://www.instagram.com/p/CLe5vMwnI6X/', 'https://www.instagram.com/p/CLe5uoFJSmv/', 'https://www.instagram.com/p/CLe5uzjjVG5/', 'https://www.instagram.com/p/CLe5uxzA3XG/', 'https://www.instagram.com/p/CLe5uwZF3YH/', 'https://www.instagram.com/p/CLe5usHDLV0/', 'https://www.instagram.com/p/CLe5uuQBXgv/', 'https://www.instagram.com/p/CLe5uhMDJm6/', 'https://www.instagram.com/p/CLe5ucTnWQX/',
                     'https://www.instagram.com/p/CLe5yDZl1do/', 'https://www.instagram.com/p/CLe5JOigLQD/', 'https://www.instagram.com/p/CLe3m35JChq/', 'https://www.instagram.com/p/CLK_KD8Hr30/', 'https://www.instagram.com/p/CIKiXlIgbU5/', 'https://www.instagram.com/p/CIBWb2bASnb/', 'https://www.instagram.com/p/CLe5-SGJEpI/', 'https://www.instagram.com/p/CLe593kBxN1/', 'https://www.instagram.com/p/CLe59tQncTD/', 'https://www.instagram.com/p/CLe59qUjXmb/', 'https://www.instagram.com/p/CLe59cDBMOB/', 'https://www.instagram.com/p/CLe572XADFx/', 'https://www.instagram.com/p/CLe57R0JUV0/', 'https://www.instagram.com/p/CLe57lGsROq/', 'https://www.instagram.com/p/CLe57p6sMm4/', 'https://www.instagram.com/p/CLe57jalapP/', 'https://www.instagram.com/p/CLe57jdnpJe/', 'https://www.instagram.com/p/CLe57A7APHX/', 'https://www.instagram.com/p/CLe56xkh-Nu/', 'https://www.instagram.com/p/CLe56tfFAwp/', 'https://www.instagram.com/p/CLe56b2Mttx/', 'https://www.instagram.com/p/CLe56P1hrzS/', 'https://www.instagram.com/p/CLe56HoMtq9/', 'https://www.instagram.com/p/CLe554ODuFN/', 'https://www.instagram.com/p/CLe55hHlf2I/', 'https://www.instagram.com/p/CLe55aRJhOF/', 'https://www.instagram.com/p/CLe5y-hFmyP/', 'https://www.instagram.com/p/CLe55M3rZQn/', 'https://www.instagram.com/p/CLe55N0p9PQ/', 'https://www.instagram.com/p/CLe55LIJCOL/', 'https://www.instagram.com/p/CLe55BMBh1B/', 'https://www.instagram.com/p/CLe54hABdQt/', 'https://www.instagram.com/p/CLe54c2ptSJ/', 'https://www.instagram.com/p/CLe5zazgfLF/', 'https://www.instagram.com/p/CLe5uERhaum/', 'https://www.instagram.com/p/CLe39K8ByMu/', 'https://www.instagram.com/p/CLdb8pzhaxU/', 'https://www.instagram.com/p/CLe54ayHf0L/', 'https://www.instagram.com/p/CLe53ygJoOd/', 'https://www.instagram.com/p/CLe54FdjeBG/', 'https://www.instagram.com/p/CLe54ABBSuI/', 'https://www.instagram.com/p/CLe5312BYCy/', 'https://www.instagram.com/p/CLe53b5hD-3/', 'https://www.instagram.com/p/CLe52yPBeqV/', 'https://www.instagram.com/p/CLe52i6sn_R/', 'https://www.instagram.com/p/CLe52YqB2h7/', 'https://www.instagram.com/p/CLe51Y7LlNK/', 'https://www.instagram.com/p/CLe51CPnCst/', 'https://www.instagram.com/p/CLe501WDkow/', 'https://www.instagram.com/p/CLe500op7AA/', 'https://www.instagram.com/p/CLe5z5xHRms/', 'https://www.instagram.com/p/CLe5zj-lF79/', 'https://www.instagram.com/p/CLe5vB6p2xF/', 'https://www.instagram.com/p/CLe5uM6pZ_r/', 'https://www.instagram.com/p/CLe5ti9FMpU/', 'https://www.instagram.com/p/CLe5YEcFcFs/', 'https://www.instagram.com/p/CLe5GqjgrKB/', 'https://www.instagram.com/p/CLe1c3XARPP/', 'https://www.instagram.com/p/CLdb7KuBpqZ/', 'https://www.instagram.com/p/CLSdSnpnCTb/', 'https://www.instagram.com/p/CLe5zAKHLxn/', 'https://www.instagram.com/p/CLe5y9rnx45/', 'https://www.instagram.com/p/CLe5uYnBhr2/', 'https://www.instagram.com/p/CLe5yDRHGAH/', 'https://www.instagram.com/p/CLe5xbcJ9pr/', 'https://www.instagram.com/p/CLe5xcUp1S9/', 'https://www.instagram.com/p/CLe5xN6HEem/', 'https://www.instagram.com/p/CLe5w8pD_5o/', 'https://www.instagram.com/p/CLe5wvyhFsy/', 'https://www.instagram.com/p/CLe5wkVpRQO/', 'https://www.instagram.com/p/CLe5v56DFZ2/', 'https://www.instagram.com/p/CLe5v0wjR5r/', 'https://www.instagram.com/p/CLe5vMwnI6X/', 'https://www.instagram.com/p/CLe5uoFJSmv/', 'https://www.instagram.com/p/CLe5uzjjVG5/', 'https://www.instagram.com/p/CLe5uxzA3XG/', 'https://www.instagram.com/p/CLe5uwZF3YH/', 'https://www.instagram.com/p/CLe5usHDLV0/', 'https://www.instagram.com/p/CLe5uuQBXgv/', 'https://www.instagram.com/p/CLe5uhMDJm6/', 'https://www.instagram.com/p/CLe5ucTnWQX/']

    return list_of_posts



def prepared_user_list():
    list_userid_1 = ['ilove.amsterdam', 'living_europeofficial', 'marlouwinkler', 'mariedpc', 'another_dam_photographer', 'amsterdamworld', 'survivaldutch', 'dalima_ss', 'marlenedeboer', 'opqrstu_graphic_design', 'phil_planespotter', 'terki_in_wonderland', 'ascoresquealuve', 'speedline_express', 'photo_graphybyabbey', 'trailer_recovery_northwest', 'melani_carmila', 'mrfleamino', 'nudiscodeeprecords', 'kelex_twinss', 'opqrstu_graphic_design', 'pure.filth.photography', 'guidofrabotta', 'ann_bochenko_art', 'albert_world_', 'kurdo_photo', 'corriethefrenchbullterrier', 'amsterdamtravelers', 'djwhizzard',
                     'misstarav', 'lacarreracyclingclub', 'mk_prodc', 'karl_heinz4life', 'allcannaart', 'parisleur', 'noreddineamjd', 'corriethefrenchbullterrier', 'casablanca.wholesale', 'abitoflemon', 'samuel.e.bostic', 'allcannaart', 'bryangarsie', 'casablanca.wholesale', 'ams.fotografie.vines', 'casablanca.wholesale', 'jessica._.allen_70', 'corriethefrenchbullterrier', 'casablanca.wholesale', 'speedline_express', 'casablanca.wholesale', 'casablanca.wholesale', 'casablanca.wholesale', 'casablanca.wholesale', 'the_cactus_home', 'casablanca.wholesale', 'reggada_and_laalaoui', 'casablanca.wholesale']

    list_userid_2 = ['nemcy.kz', 'ryrapa', '007natalee', 'best_of_sanfrancisco', 'n.lee007', 'benjamin.freemantle', 'dest0n', 'sophiarose92', 'tallyfromthevalley', 'loubelle', 'ccozycomforts', 'radenko_nikolich93', 'pitties_puppy_shop', 'sidonie_el_snake_official', 'heavenscentflowerco', 'shopjenaicollection', 'mywrld.jpg', 'nelsoncanham', 'freebies1075', 'behavioralhealthofca', 'calitrippin', 'therealmaharaj', 'kali_coach', 'dravenghostt', 'bcampbellxxi', 'phukdupnews', 'poshextensionbarhairstore', 'becky_michael_fx',
                     'fairysportss', 'dav.al45', 'drtrustenmoore', 'edwin.0498', 'wael.althan', 'gimacompany', 'bmwmgram', 'peaceful.lens', 'maze_of_fez', 'beuty_photo_feya', 'pxl8photography', 'gemstones__hub', 'michellechoates', 'knell____', 'coop_fanpage_', 'canada_ra', 'official.punjatan', 'luise.dottie', 'crimsope_tv', 'allwomenwithcurves', 'lalaily_', 'xmelimel_', 'the.lazer.viking', 'kali_khronicles', 'kaiart89', 'baysushicafe', 'lightingworld', 'sofiabass_art', 'sac_music916', 'craftgraphics.beer']

    return list_userid_1    


def tag_list():
    tag_list = ['mashad','sari','venice']
    return tag_list

if __name__ == '__main__':

    # initial action
    kill_zombies()

    # create the driver
    
    #browser = create_driver_chrome()

    # login to instagram
    #login_instagram(browser)

    # enter hashtag and collect the post links
    #links = collect_post_links(browser, 'california')

    for tag in tag_list():
        browser = create_driver()
        links = collect_post_links(browser, tag)
        insta_id_list = create_id_list(links, browser)
        #insta_id_list = prepared_user_list()
        browser = create_driver()
        fetch_user_ids(browser, insta_id_list)

    #links = prepared_post_list()

    # train the location of th user id in the post page
    #userid_learned_xpath = train_the_userid_xpath('dream__seekers', 'https://www.instagram.com/p/CKcUb-VFxWq/')

    # create list of user IDs
    #insta_id_list = create_id_list(links, browser)  # , userid_learned_xpath)
    #insta_id_list = prepared_user_list()

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
      # , trained_dict)

    close_browser(browser)
