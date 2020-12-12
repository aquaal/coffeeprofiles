# A. Quaal -- coffee_scraper.py
# Created: November 28, 2020

# This script is a webscaper to gather coffee profile attributes from Sweet Maria's, a coffee roasting company in Oakland, CA

# Import required packages
import re
import time
import requests
from bs4 import BeautifulSoup

# Make a request for currently-available coffee
url = 'https://www.sweetmarias.com/green-coffee.html?product_list_limit=all&sm_status=1&sm_type=2029'
response = requests.get(url)

# Check that there is a response
if(response.ok):
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

# Find all coffees using the class 'product-item-link'
links = soup.find_all("a", class_="product-item-link")

coffee_links = []

# Iterate through coffee <a> tags and pull out link. There are a few coffee sets on the page  that do not contain individual coffee profile attributes, so skip over those in the iteration.

for link in links:
    new_link = re.findall('href="(.*?)"', str(link))
    if len(new_link) == 0 or "sampler" in new_link[0] or "set" in new_link[0]:
        continue
    coffee_links.append(new_link)

# Repeat the same process for the coffee archive
url = 'https://www.sweetmarias.com/green-coffee.html?product_list_limit=all&sm_status=2&sm_type=2029'
response = requests.get(url)

if(response.ok):
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

links = soup.find_all("a", "product-item-link")

for link in links:
    new_link = re.findall('href="(.*?)"', str(link))
    if len(new_link) == 0 or "sampler" in new_link[0] or "set" in new_link[0]:
        continue
    coffee_links.append(new_link)

# For each coffee link, scrape the HTML and store it in a .txt file. The HTML will be processed, cleaned, and converted into a dataframe object using the 'coffee_cleaner.py' script.

# Initialize a coffee_count variable to track the number of links scraped. This allows for re-starting the process mid-list if an error is encountered
coffee_count = 0
coffee_total = len(coffee_links)

# While the coffee_count variable is lower than the length of the coffee_links list, iterate  through the coffee_links list and request each URL. This loop uses the time.time() function to create a delay based on the response time from the site -- so as not to overwhelm the site.

while coffee_count < coffee_total:
    url = coffee_links[coffee_count][0]
    t0 = time.time()
    response = requests.get(url)
    print("Harvesting coffee #{} of {}".format(coffee_count + 1, coffee_total))
    
    # If there is a response, parse the HTML and find each "product data items" instance 
    if(response.ok):
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        data_items = soup.find_all("div", "product data items")
        print("Roasting coffee #{} of {}".format(coffee_count + 1, coffee_total))
        
        # Write the data_items to a new .txt. file with the format: "coffee#.txt"        
        f = open("coffee" + str(coffee_count + 1) + ".txt", "a")
        f.write(str(data_items))
        f.close()
    
    # Calcualte the response delay and sleep for that time before incrementing and continuing
    response_delay = time.time() - t0
    print("Response delay: {}".format(response_delay))
    time.sleep(10 * response_delay)
    coffee_count += 1

print("Coffee scraping complete!")