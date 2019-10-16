# Dependencies
from bs4 import BeautifulSoup
import requests
import datetime

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo


# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.etl_project_db

# Drops collection if available to remove duplicates
db.partyCity.drop()

# Creates a collection in the database and inserts two documents

url = 'https://www.partycity.com/search?q=zombie+costumes&lang=en_US/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

#print(soup.prettify())

# results are returned as an iterable list
results = soup.find_all('li', class_="o_product-tile")


for result in results:

    try:

        title = result.find('span', class_="product-title").text

        price = result.find('div',class_="price-container").text

        url = result.a['href']

        image = result.img['data-src']
        
#         seller = result.find('p', {'data-test-info-type' :'brandName'}).text


        if (title):
            print('-------------')
            print(f"Seller: Party City")
            print(f"Product Name: {title}")
            print(f"Product URL: {url}")
            print(f"Product Image: {image}")
            print(f"Price: {price}")

        db.partyCity.insert_many(
            [
                {
                    'seller':'Party City',
                    'product':title,
                    'url':url,
                    'image':image,
                    'price':price,
                    'create_date':datetime.datetime.utcnow()
                }
            ]
        )     


    except AttributeError as e:
        print(e)