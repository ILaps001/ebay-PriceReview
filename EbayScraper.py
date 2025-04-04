#Import Dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

import re


# Define the base URL for the eBay search
url = "https://www.ebay.com/sch/i.html"

# Define the query parameters for the search request
def searchebaysetup(searchwords='',condition='',location="Domestic",Min=0,Max=1000,directory="No Directory",category="No Category",sort_order="Best Match",Sold=0,completeditems=0,BIN=0,Auction=0,BO=0,FS=0):
    ebay_filters = {
    "item_conditions": {
        '': 0,
        "New": 1000,
        "Open box": 1500,
        "Used": 3000,
        "Certified Refurbished": 2000,
        "Excellent - Refurbished": 2500,
        "Very Good": 3000,
        "Good": 4000,
        "For Parts or Not Working": 7000
    },
    "item_locations": {
        "Domestic": 1,
        "International": 2,
        "Continent": 3,
    },
    "directories": {
        "No Directory": 0,
        "Consumer Electronics": 9355,
        "Clothing, Shoes & Accessories": 11450,
        "Health & Beauty": 26395,
        "Home & Garden": 11700,
        "Sporting Goods": 382,
        "Toys & Hobbies": 220,
        "Books": 267,
        "Video Games & Consoles": 1249,
        "Collectibles": 1,
        "Business & Industrial": 12576,
        "Automotive": 6000, 
    },
    "categories": {
        "No Category": 0,

        "vintage & antique jewlery": 262024,
        "Vintage & Antique Brooches & Pins": 262004,
        "Vintage & Antique Bracelets & Charms": 262003,
        "Vintage & Antique Necklaces & Pendants":262013,
        "Vintage & Antique Collections & Lots":262016,
        "Vintage & Antique Earrings": 262008,

        "Decorative Pottery & Glassware": 262384,
        "Decorative Cookware, Dinnerware & Serveware":262364,
       

        "Cell Phones & Smartphones": 9355,
        "Laptops & Netbooks": 175673,
        "Watches": 31387,
        "Furniture": 3197,
        "Action Figures": 2605,
        "Jewelry & Watches": 281,
        "fine jewlery": 4196,
        "Fashion Jewelry": 10968,
        "vintage & antique jewlery": 262024,
        "Vintage & Antique Brooches & Pins": 262008,
        "Vintage & Antique Bracelets & Charms": 262003,
        "Vintage & Antique Necklaces & Pendants":262013,
        "Vintage & Antique Collections & Lots":262016,
        "Cameras & Photo": 625,
        "Pet Supplies": 1281,
        "Crafts": 14339,
        "Computers/Tablets & Networking": 58058,
        "Cars & Trucks": 6001,  
        "Motorcycles": 6024,  
        "Car & Truck Parts": 6030,  
        "Motorcycle Parts": 10063,  
        "Automotive Tools & Supplies": 34998,  
    },
    "sort_order": {
        "Best Match": 12,
        "Time: ending soonest": 1,
        "Time: newly listed": 10,
        "Price + Shipping: lowest first": 15,
        "Price + Shipping: highest first": 16,
        "Distance: nearest first": 7
    }
}
   #aassighn the parameters to the search 
    if (searchwords == ''):
        params = {
            '_from': 'R40',
            'LH_ItemCondition': ebay_filters["item_conditions"][condition],  # Item condition; 'New'.
            'LH_PrefLoc': ebay_filters["item_locations"][location],  # Item location; 'Domestic'."],
            '_udlo': Min,  # Minimum price.
            '_udhi': Max,  # Maximum price.
            '_dcat': ebay_filters["directories"][directory],  # Filter by directory ID; "Consumer Electronics".
            '_sacat': ebay_filters["categories"][category],  # Filter by category ID; "Cell Phones & Smartphones".
            '_sop': ebay_filters["sort_order"][sort_order],  # Sort by "Time: newly listed"
            'LH_Sold': Sold,  # Only sold listings (='1').
            'LH_Complete': completeditems,  # Only completed listings (='1').
            'LH_BIN': BIN,  # Only Buy It Now listings (='1').
            'LH_Auction': Auction,  # Only Auction Listings (='1').
            'LH_BO': BO,  # Only listings that accept offers (='1').
            'LH_FS': FS,  # Only Free Shipping listings (='1').
            '_ipg': '40',  # Number of items per page (='1'), Max is 240.
            'rt': 'nc'  # Result type; 'nc' indicates no cache to ensure the search results are fresh. 
        }
    else:
        params = {
            '_from': 'R40',
            '_nkw': searchwords,
            'LH_ItemCondition': ebay_filters["item_conditions"][condition],  # Item condition; 'New'.
            'LH_PrefLoc': ebay_filters["item_locations"][location],  # Item location; 'Domestic'."],
            '_udlo': Min,  # Minimum price.
            '_udhi': Max,  # Maximum price.
            '_dcat': ebay_filters["directories"][directory],  # Filter by directory ID; "Consumer Electronics".
            '_sacat': ebay_filters["categories"][category],  # Filter by category ID; "Cell Phones & Smartphones".
            '_sop': ebay_filters["sort_order"][sort_order],  # Sort by "Time: newly listed"
            'LH_Sold': Sold,  # Only sold listings (='1').
            'LH_Complete': completeditems,  # Only completed listings (='1').
            'LH_BIN': BIN,  # Only Buy It Now listings (='1').
            'LH_Auction': Auction,  # Only Auction Listings (='1').
            'LH_BO': BO,  # Only listings that accept offers (='1').
            'LH_FS': FS,  # Only Free Shipping listings (='1').
            '_ipg': '40',  # Number of items per page (='1'), Max is 240.
            'rt': 'nc'  # Result type; 'nc' indicates no cache to ensure the search results are fresh. 
            
        }
    return params
# Pulls extra details from a individual items page
def pullDetail(link):   
    
    response  = requests.get(link)
    html_content = response.text # Get the HTML content of the page
    soup = BeautifulSoup(html_content, 'html.parser') 

    # Parseing for seller id 
    seller=soup.find('div',class_='x-sellercard-atf__info__about-seller')
    if seller == None:
        seller="not available"
    elif seller.find_all()==[] :
        seller="not available"
    else:
        seller=seller.find('span',class_="ux-textspans ux-textspans--BOLD").text
    #Parsing for views
    views =soup.find('div',class_='ux-image-carousel-buttons ux-image-carousel-buttons__top-left')
    if views != None:   
        views = views.text
        if views == '':
            views = 'No recent views'
    #Parsing for watch count
    watch = soup.find('span',class_='x-watch-heart-btn-text')
    if watch != None:
        watch = watch.text
    else:
        watch=0
    #Parsing for image URL
    image_url =soup.find('div',attrs={'tabindex':0}).find('div',attrs={'data-idx':0}).find('img').get('src')
    description = itemsdescription(link.replace("https://www.ebay.com/itm/", ""),soup=soup)
    
    return seller,views,watch,image_url,description
def image_download (img_url,itemNum):
    # Download the image from the URL
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            # Save the image to a file
            with open(f"{itemNum}.jpg", 'wb') as f:
                f.write(response.content)
            print(f"Image for item {itemNum} downloaded successfully.")
        else:
            print(f"Failed to download image for item {itemNum}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading the image for item {itemNum}: {e}")
def similarItems(itemNum):
    similarItemId = []
    link=f"https://www.ebay.com/recs?component=lex8aspects-100-items&item_id={itemNum}"
    response  = requests.get(link)
    html_content = response.text # Get the HTML content of the page
    item_id_match = re.findall(r'"itemId":"(\d+)"', html_content)
    similarItemId = []
    for i in item_id_match:
        if i not in similarItemId:
            similarItemId.append(i)
    return similarItemId
def itemsdescription(itemNum,soup=None):
    if soup == None:
        # If soup is not provided, create a new request to get the HTML content
        link=f"https://www.ebay.com/itm/{itemNum}"
        response  = requests.get(link)
        html_content = response.text # Get the HTML content of the page
        soup = BeautifulSoup(html_content, 'html.parser')
    # Parseing for items description
    descriptionsouop=soup.find('div',class_="ux-layout-section-evo ux-layout-section--features")
    if descriptionsouop!= None:
        subsets=descriptionsouop.find_all('div',class_="ux-layout-section-evo__row")
        description=[]
        for x in subsets:
            catagories=x.find_all('div',class_="ux-layout-section-evo__col")
            for y in catagories:
                if y.find(class_="ux-labels-values__values") == None:
                    break
                value=y.find(class_="ux-labels-values__values").find('span',class_='ux-textspans').text
                lable=y.find(class_="ux-labels-values__labels").find('span',class_="ux-textspans").text
                description.append((lable,value))
    else:
        description = None
    return description 

# Function to search eBay and return a DataFrame of items
def searchEbay(searchwords='',condition='',location="Domestic",Min=0,Max=1000,directory="No Directory",category="No Category",sort_order="Best Match",Sold=0,completeditems=0,BIN=0,Auction=0,BO=0,FS=0):
    
    params = searchebaysetup(searchwords,condition,location,Min,Max,directory,category,sort_order,Sold,completeditems,BIN,Auction,BO,FS)
    request =requests.Request('GET', url, params=params)
    prepared_request = request.prepare()
    print()
    print(f"URL OF SEARCH: {prepared_request.url}")

    # Initialize variables
    page_number = 0
    items_list = []

    # Loop over pages
    while True: 

        # Increment the page number 
        page_number += 1
        params['_pgn'] = page_number

        #help with volume for broad searches 
        if page_number > 10:
            break
        
        # Send GET request to eBay with the defined parameters
        response  = requests.get(url, params=params)
        html_content = response.text # Get the HTML content of the page
        soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML content using BeautifulSoup
        
        # Finds the search result number
        if page_number == 1:
            if not(soup.find('div',class_="srp-river-answer srp-river-answer--REWRITE_START")):
                nubResultsholder = soup.find('h1',class_="srp-controls__count-heading")
                if  nubResultsholder.find('span',class_='BOLD'):
                    nubResults=nubResultsholder.find('span',class_='BOLD').text
                else:
                    nubResults=nubResultsholder.text
                print(f"Total search results: {nubResults}")
                if nubResults == '0':
                    print('No results found')
                    break
            else:
                print('No results found')
                break
        print(f'Scraping page: {page_number}')
        # Extract items from page
        items = soup.find_all('div', class_='s-item__wrapper clearfix')

        #Finds code for sponsored items 
        # (based on understaning first items are sponsored for any page for best match sort and last 2 for other sorts)
        if params['_sop']==12:
            #Finds code for sponsored items (based on understaning first 5 items are sponsored for any page)
            sponsoredItem =items[2].find_all('div',class_='s-item__detail s-item__detail--primary')
            SpID=sponsoredItem[len(sponsoredItem)-1].find_all('span')[1].get('class')[0]
        else:
            sponsoredItem =items[len(items)-1].find_all('div',class_='s-item__detail s-item__detail--primary')
            SpID=sponsoredItem[len(sponsoredItem)-1].find_all('span')[1].get('class')[0]

        # Extract Listings
        for item in items [2:]:
            title = item.find('div', class_='s-item__title').text
            price = item.find('span', class_='s-item__price').text
            link = item.find('a', class_='s-item__link')['href'].split('?')[0]

            sponsored =item.find_all('div',class_='s-item__detail s-item__detail--primary')
            sponsored=sponsored[len(sponsored)-1].find_all('span',class_=SpID)
            if len(sponsored) == 0:
                sponsored = 'No'
            else:
                sponsored = 'Yes'

            seller,views,watch,image_url,description=pullDetail(link)
            # Define each item as a dictionary
            item_dict = {
                # Extract relevant data from the item
                    'Item Number': link.replace("https://www.ebay.com/itm/", ""),  # Extract item number from the URL
                    'Title': title,
                    'Price': price,
                    'Link': link,
                    'watching': watch,
                    'seller': seller,
                    'views': views,
                    'Sponsored': sponsored,
                    'description': description,
                    'Image Link': image_url
                }
            # Append the dictionary to the list
            items_list.append(item_dict)
        if soup.find_all('div', class_='s-pagination__container') == []:
            print('only one page')
            break
        else:
            if not(soup.find_all('a', class_='pagination__next')):
                print('no more pages')
                break
    items_df = pd.DataFrame(items_list)
    return items_df

def imagedownload (items_df):
    for i in range(len(items_df)):
        image_download (items_df['Image Link'][i],items_df['Item Number'][i])

#print(itemsdescription("356725862714"))

"""
"items_df=searchEbay(searchwors="grape" ,category="Vintage & Antique Brooches & Pins",Sold=1)
data = "/Users/isabellalapsley/Desktop/ebay-PriceReview/data"
path=os.path.join(data, 'test.csv')
items_df.to_csv(path)"
"""