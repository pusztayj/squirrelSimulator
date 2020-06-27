
import csv

class ItemManager():

    # The singleton instance variable
    _INSTANCE = None
   
    @classmethod
    def getInstance(cls):
        """Used to obtain the singleton instance"""
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._IM()
        return cls._INSTANCE

    class _IM():

        def __init__(self):
    
            with open("resources\data\items.csv") as file:
                reader = csv.reader(file, delimiter=",")
                self._items = {}
                for x, row in enumerate(reader):
                    item = row[0]
                    if x == 0:
                        fields = row
                    else:
                        temp = {}
                        for c in range(1,len(row)):
                            
                            value = row[c]
                            field = fields[c]
                            
                            if value == "null":
                                temp[field] = None
                            elif value.isdigit():
                                temp[field] = int(value)
                            elif value.replace(".","",1).isdigit():
                                temp[field] = float(value)
                            elif value.lower() in ("true","false"):
                                temp[field] = value.lower() == "true"
                            else:
                                temp[field] = value

                            self._items[item] = temp

        def getAttributes(self, item):
            return self._items[item]

        def getItems(self):
            return self._items.keys()

        def getItemsByType(self, t):
            return [k for k,v in self._items.items() if v["type"]==t]

            
ITEMS = ItemManager.getInstance()
