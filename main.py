import os,random,sys,time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from IPython.display import Markdown, display

def printmd(string):
    display(Markdown(string))

driver = webdriver.Chrome('driver/chromedriver.exe')

driver.get('https://www.linkedin.com/uas/login')

time.sleep(3)
elementID = driver.find_element_by_id('username')
print("Email or Phone -")
username = input()
elementID.send_keys(username)

elementID = driver.find_element_by_id('password')
print("password -")
password = input()
elementID.send_keys(password)

elementID.submit()

print("LinkedIn profile link -")
lnk = input()
driver.get(lnk)

print("\n")

SCROLL_PAUSE_TIME = 2
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(5)

NAME = driver.find_element_by_xpath("//li[@class='inline t-24 t-black t-normal break-words']")
print("NAME:- "+ NAME.text)

# CONNECTION_TYPE = driver.find_element_by_xpath("//span[@class='dist-value']")
# print("CONNECTION_TYPE:- "+ CONNECTION_TYPE.text+" degree connection")

POSITION = driver.find_element_by_xpath("//h2[@class='mt1 t-18 t-black t-normal break-words']")
print("POSITION:- "+ POSITION.text)

LOCATION= driver.find_element_by_xpath("//li[@class='t-16 t-black t-normal inline-block']")
print("LOCATION:- "+ LOCATION.text)

time.sleep(3)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
time.sleep(5)    
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pv-profile-section__card-action-bar")))

activity = driver.find_element_by_xpath("//a[@data-control-name='recent_activity_details_all']")
driver.get(activity.get_attribute('href'))

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pv-recent-activity-detail__pills")))
nav = driver.find_element_by_xpath("//nav[@class='pv-recent-activity-detail__pills mt4']")
articles = nav.find_elements_by_tag_name('button')
articles[1].click()
time.sleep(3)

url = driver.current_url
driver.get(url)

SCROLL_PAUSE_TIME = 2
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height    

try:
    box = []
    soup = BeautifulSoup(driver.page_source,'html.parser')
    divTag = soup.find("div", {"class": "ember-view"})
    tags = soup.find_all("article", {"class": "pv-post-entity--detail-page-format artdeco-container-card pv-post-entity pv-post-entity--detailed ember-view"})
    for tag in tags:
        box.append(tag.find('a').get('href'))
    main_link = "https://www.linkedin.com"
    for i in box:
        driver.get(main_link+i)

        SCROLL_PAUSE_TIME = 2
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "reader-article-header__title")))
        a = driver.find_element_by_xpath("//h1[@dir='ltr']")
        print("Heading:-"+" "+a.text)
        print("\n")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "reader-article-content")))
        a = driver.find_element_by_xpath("//div[@class='reader-article-content']")
        paragraphs = a.find_elements_by_tag_name('p')

        for paragraph in paragraphs:
            print(paragraph.text)

        print("**END**")
        print("\n")

except:
    print("**WARNING:-you have close the chrome test browser or no article post yet.**")
