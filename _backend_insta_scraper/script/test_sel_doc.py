from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
print('imports done')

options = Options()
options.headless = True
print('going to call firefox')
d = webdriver.Firefox() #options=options)

print('# web driver initiated')



d.get("https://www.instagram.com/topdown/")
print('# title: '+str(d.title))

'''
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
'''
