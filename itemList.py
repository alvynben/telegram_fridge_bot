import foodItem

class ItemList:
    def __init__(self):
        self.itemList = []
    
    def add(self, foodItem : foodItem.FoodItem):
        self.itemList.append(foodItem)
    
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