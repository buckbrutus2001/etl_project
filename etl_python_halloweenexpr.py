# Dependencies
from bs4 import BeautifulSoup
import requests

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo


# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.etl_project_db

# Drops collection if available to remove duplicates
db.halloweenExpress.drop()

# Creates a collection in the database and inserts two documents

url = 'https://www.halloweenexpress.com/adult-costumes/zombie-costumes/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

#print(soup.prettify())

# results are returned as an iterable list
results = soup.find_all('li', class_="product")


for result in results:

    try:

        title = result.find('h4', class_="card-title").text

        price = result.find('span',class_="price").text

        url = result.a['href']

        image = result.img['data-src']

        seller = result.find('p', {'data-test-info-type' :'brandName'}).text


        if (title):
            print('-------------')
            print(f"Seller: {seller}")
            print(f"Product Name: {title}")
            print(f"Product URL: {url}")
            print(f"Product Image: {image}")
            print(f"Price: {price}")

        db.halloweenExpress.insert_many(
            [
                {
                    'seller':seller,
                    'product':title,
                    'url':url,
                    'image':image,
                    'price':price
                }
            ]
        )     


    except AttributeError as e:
        print(e)