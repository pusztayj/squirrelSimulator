
import csv, re

class AbstractManager():

    def __init__(self, files, ds, lower=True, toLyst=[]):
        if type(files)==str and type(ds)==dict:
            files = [files]
            ds = [ds]
        assert len(files) == len(ds)
        for n, f in enumerate(files):
            with open("resources/data/" + f) as file:
                reader = csv.reader(file, delimiter=",")
                for x, row in enumerate(reader):
                    obj = row[0]
                    if lower: obj = obj.lower()
                    if x == 0:
                        fields = row
                    else:
                        temp = {}
                        for c in range(1,len(row)):
                            
                            value = row[c]
                            field = fields[c]

                            # Normalize and format the different data types
                            rangeMatch = re.match("\(([\d]+)-([\d]+)\)", value)
                            rgbMatch = re.match("\(([\d]+),[ ]?([\d]+),[ ]?([\d]+)\)", value)
                            if rangeMatch:
                                temp[field] = (int(rangeMatch.group(1)),
                                               int(rangeMatch.group(2)))
                            elif rgbMatch:
                                temp[field] = (int(rgbMatch.group(1)),
                                               int(rgbMatch.group(2)),
                                               int(rgbMatch.group(3)))
                            elif value == "null":
                                temp[field] = None
                            elif value.isdigit():
                                temp[field] = int(value)
                            elif value.replace(".","",1).isdigit():
                                temp[field] = float(value)
                            elif value.lower() in ("true","false"):
                                temp[field] = value.lower() == "true"
                            else:
                                temp[field] = value

                        # Check if the result dictionary should be appended to a list
                        if n in toLyst:
                            if obj in self._menuButtons.keys():
                                ds[n][obj].append(temp)
                            else:
                                ds[n][obj] = [temp]
                        else:
                            ds[n][obj] = temp
        
