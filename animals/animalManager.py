import csv

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
                        self._animals[species] = {fields[c]:int(row[c])
                                if row[c].isdigit()
                                else row[c] for c in range(1,len(row))}

        def getStats(self, animal):
            return self._animals[animal]

ANIMALS = AnimalManager.getInstance()
