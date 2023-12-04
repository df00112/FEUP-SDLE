import random
from PNCounter import PNCounter
import sys
class Item:
    def __init__(self, name, quantity,status):
        self.name = name
        self.quantity = PNCounter(quantity)
        self.bought_status = PNCounter(status) # 0 = not bought, 1 = bought
    
    def inc_quantity_negative_counter(self,quantity):
        self.quantity.decrement(quantity)
        
    def inc_bought_status_negative_counter(self,status):
        self.bought_status.decrement(status)
              
class AWORSet:
    def __init__(self,list_id, list_name, user_id,counter=1):
        self.list_id=list_id
        self.list_name=list_name
        self.owner=user_id
        self.cCounter=counter
        self.context=set()
        self.items = dict()

    
    def add_existing(self,item_key,quantity,bought_status):
        self.items[item_key]=Item(item_key[0],quantity,bought_status)
        

    def add_new(self,item_name,quantity,bought_status):
        item = Item(item_name,quantity,bought_status)
        self.context.add((item_name,self.cCounter))
        self.items[(item_name,self.cCounter)]=item
        self.cCounter+=1

    def remove(self,item_name):
        
        min_counter=sys.maxsize
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
    
    def all_info(self):
        print("List ID:", self.list_id)
        print("List Name:", self.list_name)
        print("Owner:", self.owner)
        print("Counter:", self.cCounter)
        print("\nContext:")
        for context_item in self.context:
            print(context_item)
        self.lookup()
    
    def get_items_names(self):
        items_names=[]
        for key in self.items:
            items_names.append(key[0])
        return items_names
        
    def lookup(self):
        print("Items:")
        for key in self.items:
            status=self.items[key].bought_status.lookup()
            text = "not bought" if status == 0 else "bought"
            print(key[0],"-", self.items[key].quantity.lookup(),"-",text)

# Example usage
""" shopping_list = AWORSet(12312,"carralista","AAAAHHHAHAHAHA")
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
shopping_list.lookup() """
