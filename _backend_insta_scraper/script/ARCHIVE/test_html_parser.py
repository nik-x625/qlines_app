from bs4 import BeautifulSoup as bs
import sys


with open('the_page_source4_hashtag_result.html', 'r') as f:
    webpage = f.read()#.decode('utf-8')

soup = bs(webpage)

res = soup.find('article')
print(res)