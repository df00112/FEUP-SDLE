import random
from PNCounter import PNCounter
import sys
class Item:
    def __init__(self, name, quantity, bought_status):
        self.name = name
        self.quantity = PNCounter(quantity)
        self.bought_status = PNCounter(bought_status) # 0 = not bought, 1 = bought
        
              
class AWORSet:
    def __init__(self,list_id, list_name, user_id):
        self.list_id=list_id
        self.list_name=list_name
        self.owner=user_id
        self.cCounter=1
        self.context=set()
        self.items = dict()

    def add(self,item_name,quantity,bought_status):
        item = Item(item_name,quantity,bought_status)
        self.context.add((item_name,self.cCounter))
        self.items[(item_name,self.cCounter)]=item
        self.cCounter+=1

    def remove(self,item_name):
        
        min_counter=sys.maxint
        key_to_remove=None
        for key in self.items:
            if key[0]==item_name:
                if key[1]<min_counter:
                    min_counter=key[1]
                    key_to_remove=key
        
        if key_to_remove!=None:
            del self.items[key_to_remove]
            
                    
    def join(self,otherList):
        for context in otherList.context:
            if context not in self.context:
                self.context.add(context)
                self.items[context]= otherList.items.get(context, None)
            else:
                if otherList.items.get(context) is None:
                    self.remove(context[0])
                else:
                    self.items[context].quantity.merge(otherList.items[context].quantity)
                    self.items[context].bought_status.merge(otherList.items[context].bought_status)
        
        self.cCounter=max(self.cCounter,otherList.cCounter)
            
    def update_item_quantity(self,item_name,quantity):
        for key in self.items:
            if key[0]==item_name:
                self.items[key].quantity.update_quantity(quantity)
                return
        
    def update_item_status(self,item_name,status):
        for key in self.items:
            if key[0]==item_name:
                self.items[key].bought_status.update_status(status)
                return
    

    def lookup(self):
        for key in self.items:
            status=self.items[key].bought_status.lookup()
            text = "not bought" if status == 0 else "bought"
            print(key[0],"-", self.items[key].quantity.lookup(),"-",text)

# Example usage
shopping_list = AWORSet(12312,"carralista","AAAAHHHAHAHAHA")
shopping_list.add("Apples", 50,1)  
shopping_list.add("Bananas", 10,0)


shopping_list2 = AWORSet(12312,"carralista","AAAAHHHAHAHAHA")
shopping_list2.add("Apples", 50,1)
shopping_list2.add("Bananas", 10,0)
shopping_list2.add("Oranges", 10,1)
shopping_list2.remove("Bananas")
shopping_list2.update_item_quantity("Apples", 100)
shopping_list2.update_item_status("Apples", 0)
shopping_list2.update_item_status("Apples", 1)
shopping_list2.update_item_status("Apples", 0)
shopping_list2.update_item_quantity("Apples", 50)
shopping_list2.update_item_quantity("Apples", 75)
shopping_list2.add("Bananas", 20,0)


shopping_list.join(shopping_list2)

print("Current shopping list:")
shopping_list.lookup()