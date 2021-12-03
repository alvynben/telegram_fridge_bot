import json
from data.foodItem import FoodItem
import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']

class Storage:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS public.fridgedata (id bigserial NOT NULL, name varchar NOT NULL, expiry timestamp NOT NULL, PRIMARY KEY (id))')
    
    def initialise_foodList(self, foodList):
        self.cur.execute('SELECT name,expiry from public.fridgedata')
        for entry in self.cur.fetchall():
            foodList.itemList.append(FoodItem(entry[0],entry[1]))
    
    def add(self, foodItem : FoodItem):
        self.cur.execute('SET DATESTYLE = dmy;')
        self.cur.execute('INSERT INTO public.fridgedata (name, expiry) VALUES (%s, %s)',
        (foodItem.name, foodItem.expiry))
    
    def getMatchingItemsByName(self,name):
        regexp = '%' + name + '%'
        self.cur.execute('SELECT id,name,expiry from public.fridgedata WHERE name LIKE %s',(regexp,))
        matchingItems = []
        for entry in self.cur.fetchall():
            matchingItems.append({
                'id': entry[0],
                'name': entry[1],
                'expiry': entry[2] 
            })
        
        return matchingItems
    
    def getItemByIndex(self,index) -> FoodItem:
        try:
            self.cur.execute('SELECT name,expiry from public.fridgedata WHERE id = %s',(index,))
            name, expiry = self.cur.fetchone()
            return FoodItem(name,expiry)
        except:
            self.conn.rollback()
            return 0

    def removeByIndex(self, index):
        try:
            self.cur.execute('DELETE FROM public.fridgedata WHERE id = %s',(index,))
            return 1
        except:
            self.conn.rollback()
            return 0

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
