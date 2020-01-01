# LOAD MODULES #
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

# PREPARE .CSV TO STORE PROFILE DETAILS #
exportcsv = open('Profiles.csv', 'w', newline='', encoding='utf-8')
csvwriter = csv.writer(exportcsv)
csvwriter.writerow(['ID', 'Company Name', 'Short Description', 'Industry', 'Website', 'Phone', 'Size', 'HQ', 'Founded', 'Specialties', 'LinkedIn Profile Page'])

# CREDENTIALS #
username = '' # Insert your credentials here
password = '' # Insert your credentials here

# CHROME PREPARATION AND TARGET DEFINITION #
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

# LOAD COMPANY PAGES #
def csv_url_reader(url_obj):
    reader = csv.DictReader(url_obj, delimiter = ',')
    for line in reader:
        url = line['Link']
        driver.get(url)
        time.sleep(5)

# PARSE DATA #
        profilepage = driver.current_url
        about = driver.find_element_by_link_text('About').click()
        time.sleep(3)
        companyname = driver.title
        companyname = companyname.split(': About')[0]
        ID = profilepage.split('/company/')[1]
        ID = ID.replace('/about/', '')
        ID = ID.replace('/', '')

        try:
            top = driver.find_element_by_class_name("org-top-card__left-col")
            shortdesc = top.find_element_by_tag_name("p").text.strip()
        except Exception as e:
            shortdesc = 'N/A'

        try:
            website = driver.find_element_by_xpath("//dt[text()='Website']/following-sibling::dd").text.strip()
        except Exception as e:
            website = 'N/A'

        try:
            phone = driver.find_element_by_xpath("//dt[text()='Phone']/following-sibling::dd").text.strip()
            phone = phone.split('\n')[0]
        except Exception as e:
            phone = 'N/A'

        try:
            industry = driver.find_element_by_xpath("//dt[text()='Industry']/following-sibling::dd").text.strip()
        except Exception as e:
            industry = 'N/A'

        try:
            size = driver.find_element_by_xpath("//dt[text()='Company size']/following-sibling::dd").text.strip()
            size = size.replace(',', '')
        except Exception as e:
            size = 'N/A'

        try:
            hq = driver.find_element_by_xpath("//dt[text()='Headquarters']/following-sibling::dd").text.strip()
            hq = hq.replace(',', '')
        except Exception as e:
            hq = 'N/A'

        try:
            founded = driver.find_element_by_xpath("//dt[text()='Founded']/following-sibling::dd").text.strip()
        except Exception as e:
            founded = 'N/A'

        try:
            specialties = driver.find_element_by_xpath("//dt[text()='Specialties']/following-sibling::dd").text.strip()
        except Exception as e:
            specialties = 'N/A'

        print(ID)
        print(companyname)
        print(shortdesc)
        print(industry)
        print(website)
        print(phone)
        print(size)
        print(hq)
        print(founded)
        print(specialties)
        print(profilepage)

# EXPORT PROFILE DETAILS TO .CSV #
        csvwriter.writerow([ID, companyname, shortdesc, industry, website, phone, size, hq, founded, specialties, profilepage])

if __name__ == '__main__':
    with open ('Links.csv') as url_obj:
        csv_url_reader(url_obj)

exportcsv.close()

driver.close()
