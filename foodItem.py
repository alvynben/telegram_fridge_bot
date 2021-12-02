from datetime import datetime
from dateutil.parser import parse

class FoodItem:
    def __init__(self, name, expiry : str):
        self.name = name
        self.expiry = parse(expiry, dayfirst=True)
    
    def __init__(self, name, expiry : datetime):
        self.name = name
        self.expiry = expiry
    
    def getExpiry(self):
        print(self.expiry)
    
    def isExpiryEarlierThan(self, otherFood):
        if self.expiry < otherFood.expiry:
            # print(f'{self.name} is earlier than {otherFood.name}')
            return True
        else:
            # print(f'{otherFood.name} is earlier than {self.name}')
            return False
    
    def __str__(self):
        return f'{self.name} | {self.expiry.strftime("%d %b %Y")}'
    
    def jsonFormat(self):
        return {
            'name' : self.name,
            'expiry' : self.expiry.strftime("%d/%m/%y")
        }


# burger = FoodItem("burger", "11/11/2021")
# chicken = FoodItem("chicken", "10/10/2021")
# dog = FoodItem("dog", "13/12/2021")
# burger.getExpiry()
# chicken.getExpiry()
# dog.getExpiry()

# burger.isExpiryEarlierThan(chicken)
# burger.isExpiryEarlierThan(dog)
