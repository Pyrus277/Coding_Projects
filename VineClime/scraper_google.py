import shelve
import random
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

## SFSG! This works great when the google search results are the expected format. 

# Grab the winery list from the jupyter file -- the actual winery variable
with shelve.open('wineries') as shelfFile:
    # "unshelf" the wineries varible made in the Reviews notebook 
    wineries = shelfFile['na_lst']
    
    # shelfFiles used in this scraper must be pre-initialized (been doing this in jupyter as needed)

    # This will update a list of tuples, and will be what you need to engineer a county column in the 
    # reviews df. It'll be converted into a dictionary, but using this format now so I can more easily
    # stop and pick up where I left off, if the scraper gets interrupted

    # Create a Selenium driver and open up a web page using a URL that searches for the winery
    chrome_options = Options()  
    chrome_options.add_experimental_option("detach", True) # set it up so the browser doesn't close immedately. 
    driver = webdriver.Chrome(options=chrome_options) # instantiate a chrome driver object

    # Iterate for each winery-- put winery in the with_counties list
    for i, winery in enumerate(wineries[1:]):
        url_base = 'https://www.google.com/search?q='
        # url = f"{url_base}{winery} winery".replace(' ','+')
        # Alternate search format:
        url = f"{url_base}{winery} vineyards california location".replace(' ','+')
        print('')
        print(f'Searching: {winery}')
        
        # "google search" for the winery
        driver.get(url)
        driver.implicitly_wait(10) # implicit sleep time to give the browser a chance to load everything
        time.sleep(random.uniform(1,2))# minimum sleep time so we don't get in trouble for scraping

        # Now we're gonna go in and pluck out the city name
        try:
            addr = driver.find_element(By.CLASS_NAME, "LrzXr").text # wow this actually this worked. Now we just gotta SLICE
            city = addr.split(',')[1][1:]
        except:
            # append to the record that we don't know the county (for now)
            shelfFile['with_counties3'] += [(winery, 'NA')]
            print(f"Couldn't find city for {winery}")
            continue
        print(f'City for {winery} is {city}')

        # Now we need to take the city name and google search with that to find the county
        # Make a new url
        url_base = 'https://www.google.com/search?q='
        url = f"{url_base}{city} Ca county".replace(' ','+')
        # print(url)

        # Use our driver to now "search" this URL
        driver.get(url) # open up the second url
        driver.implicitly_wait(10) # implicit sleep time to give the browser a chance to load everything
        time.sleep(random.uniform(1,2))
        
        try:
            # grab the county name
            county = driver.find_element(By.CSS_SELECTOR, "div[class='SPZz6b'] > h2 ").text
        except: 
            # append to the record that we don't know the county (for now)
            shelfFile['with_counties3'] += [(winery, 'NA')]
            print(f"Couldn't find county for {winery}")
            continue
        print(f'County for {winery} is {county}')

        # if all goes well for the iteration, we get to update the shelfFile. This is the declicious data.
        shelfFile['with_counties3'] += [(winery, county)]
        # printing 'i' so if the program crashes, we can just run the loop from the most recently completed index number
        print(f"the last index in the winery list was: {i}") 

print("Scraping complete! Check out the shelved 'with_counties' list")
driver.quit()

'''
1. Google: f"{wineries[x]} + 'winery'"
2. Get the address from the left sidebar, and store `city`
    -if the left sidebar not there, throw error
3. Google: f"{city} + 'ca county'" (or something else!)
4. Grab the `county` from the big bold letters
    -if the big bold letters not there, throw error
5. Load add to dictionary: k = wineries[x], v = `county`
'''

