import foodItem

class ItemList:
    def __init__(self):
        self.itemList = []
    
    def add(self, foodItem : foodItem.FoodItem):
        self.itemList.append(foodItem)
    
    def getList(self):
        return self.itemList
    
    def getListAsString(self):
        return "\n".join([str(food) for food in self.itemList])