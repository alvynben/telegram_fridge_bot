from data.foodItem import FoodItem
from data.storage import Storage

class ItemList:
    def __init__(self):
        self.itemList = []
        self.storage = Storage()
        self.storage.initialise_foodList(self)
    
    def add(self, foodItem : FoodItem):
        self.itemList.append(foodItem)
        self.storage.add(foodItem)
        self.storage.save()
    
    def removeByIndex(self,index):
        response = self.storage.removeByIndex(index)
        if response == 0:
            return 0
        else:
            self.storage.save()
            self.itemList = []
            self.storage.initialise_foodList(self)
            return 1

    def getByIndex(self,index) -> FoodItem:
        return self.storage.getItemByIndex(index)
    
    def getList(self):
        return self.itemList
    
    def sortBy(self, sortType):
        if sortType == "e":
            return sorted(self.itemList, key=lambda x: x.expiry)
        else:
            return self.itemList
    
    def getListAsString(self, sortType):
        newList = self.sortBy(sortType)
        return "\n".join([str(food) for food in newList])
    
    def getMatchingItemsByName(self,name):
        matchingItems = self.storage.getMatchingItemsByName(name)
        return matchingItems
    
    def getMatchingItemsByNameAsString(self,name):
        matchingItems = self.storage.getMatchingItemsByName(name)
        finalString = ''
        for item in matchingItems:
            finalString += f"{item['id']}. {item['name']} | {item['expiry']}\n"
        return finalString
