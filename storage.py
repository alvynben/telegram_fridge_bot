import json
from foodItem import FoodItem
from itemList import ItemList
import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']

class Storage:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # self.conn = psycopg2.connect("dbname=alvynben user=alvynben password=test123")
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS public.fridgedata (id bigserial NOT NULL, name varchar NOT NULL, expiry timestamp NOT NULL, PRIMARY KEY (id))')
    
    def initialise_foodList(self, foodList : ItemList):
        self.cur.execute('SELECT name,expiry from public.fridgedata')
        for entry in self.cur.fetchall():
            foodList.add(FoodItem(entry[0],entry[1]))
    
    def add(self, foodItem : FoodItem):
        self.cur.execute('SET DATESTYLE = dmy;')
        self.cur.execute('INSERT INTO public.fridgedata (name, expiry) VALUES (%s, %s)',
        (foodItem.name, foodItem.expiry))

    def save(self):
        self.conn.commit()
    
    def close(self):
        self.cur.close()
        self.conn.close()

# storage = Storage()
# storage.save()

# foodList = ItemList()
# storage.initialise_foodList(foodList)
# print(foodList.getListAsString())


# storage = Storage()

# burger = FoodItem("burger", "11/11/2021")
# chicken = FoodItem("chicken", "10/10/2021")
# dog = FoodItem("dog", "13/12/2021")
# cat = FoodItem("cat", "10/10/2020")

# storage.add(cat)

# storage.save()

# itemList = ItemList()

# itemList.add(burger)
# itemList.add(chicken)
# itemList.add(dog)

# storage.save(itemList.itemList)
# print(storage.load())
