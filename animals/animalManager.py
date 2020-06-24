import re, csv

class AnimalManager():

    # The singleton instance variable
    _INSTANCE = None
   
    @classmethod
    def getInstance(cls):
        """Used to obtain the singleton instance"""
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._AM()
        return cls._INSTANCE

    class _AM():

        def __init__(self):

            with open("animals/animals.csv") as file:
                reader = csv.reader(file, delimiter=",")
                self._animals = {}
                for x, row in enumerate(reader):
                    species = row[0].lower()
                    if x == 0:
                        fields = row
                    else:
                        temp = {}
                        for c in range(1,len(row)):
                            
                            value = row[c]
                            field = fields[c]
                            
                            match = re.match("\(([\d]+)-([\d]+)\)", value)
                            if match:
                                temp[field] = (int(match.group(1)),
                                               int(match.group(2)))
                            elif value.isdigit():
                                temp[field] = int(value)
                            elif value.lower() in ("true","false"):
                                temp[field] = value.lower() == "true"
                            else:
                                temp[field] = value

                            self._animals[species] = temp
                            
        def getStats(self, animal):
            return self._animals[animal]

        def getSpawnableAnimals(self):
            return [k for k,v in self._animals.items() if v["spawnable"]]

        def getMerchantRaces(self):
            return [k for k,v in self._animals.items() if v["merchant"]]

ANIMALS = AnimalManager.getInstance()
