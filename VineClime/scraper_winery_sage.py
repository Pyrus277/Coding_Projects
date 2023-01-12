import shelve
import random
import time
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# Create a Selenium driver and open up a web page using a URL that searches for the winery
chrome_options = Options()  
chrome_options.add_experimental_option("detach", True) # set it up so the browser doesn't close immedately. 
driver = webdriver.Chrome(options=chrome_options) # instantiate a chrome driver object
url = 'https://www.winery-sage.com/data/clienteallwines_view.php'
driver.get(url)

page = 1
with_counties_update = []

for i in range(82): # 82 because there are 81 table pages to scrape
    # do your scraping for the page

    wineries = [elem.text for elem in driver.find_elements(By.XPATH, "//*[contains(@id, 'WineryMaster.WineryName')]")]
    counties = [elem.text for elem in driver.find_elements(By.XPATH, "//*[contains(@id, 'WineryMaster.County')]")]
    # every other element in these lists are what you want to collect and pair up in tuples
    # both these lists should be the same length
    print(f'page {page}, {len(wineries)==len(counties)}')
    page+=1

    for i in range(0,len(wineries), 2):
        with_counties_update.append((wineries[i], counties[i]))
    
    time.sleep(2)
    # click the next button (this part works!) 
    linkElem = driver.find_element(By.ID, "Next")
    linkElem.click()

print(with_counties_update)

with shelve.open('wineries') as shelfFile:
    shelfFile['with_counties_update_test'] = with_counties_update 

driver.quit()

print("Scraping complete! Audit that variable")


