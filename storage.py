import json
from foodItem import FoodItem

class Storage:
    def __init__(self):
        self.STORAGE_LOCATION = 'data.txt'
    
    def save(self, lst):
        data = [item.jsonFormat() for item in lst]
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile, indent=4)
    
    def load(self):
        with open(self.STORAGE_LOCATION) as json_file:
            data = json.load(json_file)
        return data

# storage = Storage()

# burger = FoodItem("burger", "11/11/2021")
# chicken = FoodItem("chicken", "10/10/2021")
# dog = FoodItem("dog", "13/12/2021")

# itemList = ItemList()

# itemList.add(burger)
# itemList.add(chicken)
# itemList.add(dog)

# storage.save(itemList.itemList)
# print(storage.load())
