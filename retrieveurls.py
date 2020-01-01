# LOAD MODULES #
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import csv

# PREPARE .CSV TO STORE PROFILE LINKS #
exportcsv = open('Links.csv', 'w', newline='')
csvwriter = csv.writer(exportcsv)
csvwriter.writerow(['Link'])

# CREDENTIALS #
username = '' # Insert your credentials here
password = '' # Insert your credentials here

# CHROME PREPARATION AND TARGET DEFINITION #
pages = [25, 50, 75, 100, 125, 150]
chrome = r"""C:\Users\HP\Desktop\chromedriver.exe""" # ChromeDriver is needed, define the path here
driver = webdriver.Chrome(chrome)
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
time.sleep(2)
driver.maximize_window()
time.sleep(2)

# LOGIN #
login = driver.find_element_by_xpath('//*[@id="username"]')
login.send_keys(username)
time.sleep(2)
login = driver.find_element_by_xpath('//*[@id="password"]')
login.send_keys(password)
time.sleep(2)
login.send_keys(Keys.RETURN)
time.sleep(2)

# RETRIEVE COMPANY LINKS FROM JOB POSTS #
for page in pages:
    load = driver.get('https://www.linkedin.com/jobs/search/?keywords=sfdc&sortBy=DD&start={}'.format(page))
    time.sleep(5)
    scroll = driver.find_element_by_class_name('jobs-search-results')
    scroll.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    scroll.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    scroll.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    scroll.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    scroll.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    scroll.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    scroll.send_keys(Keys.PAGE_DOWN)
    time.sleep(5)

    links = driver.find_elements_by_xpath("//a[(contains(@href,'/company/')) and not(contains(@href,'setup'))]")
    for ii in links:
        print(ii.get_attribute('href'))

# EXPORT COMPANY LINKS TO .CSV #
        csvwriter.writerow([ii.get_attribute('href')])

exportcsv.close()

driver.close()

# REMOVE DUPLICATE ENTRIES #
df = pd.read_csv('Links.csv')
df.drop_duplicates(subset=None, inplace=True)
df.to_csv('Links.csv', index=False)