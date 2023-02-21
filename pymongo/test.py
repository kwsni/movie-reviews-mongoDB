import pymongo
from pprint import pprint

client = pymongo.MongoClient("-insert MongoDB connection string-")
db = client["movies"]
reviews = db["reviews"]

def use8():
  q8 = {"movie":{"$regex":"2005"}}
  t8 = list(reviews.find(q8).sort("rating", 1).limit(10))
  for x in q8:
    pprint(x)

use8()