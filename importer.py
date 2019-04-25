import csv

def importData(fileName):
    with open(fileName, mode='r') as data:
        reader = csv.reader(data)
        next(reader)
        out = [dict({'name':rows[-3],'cost':int(rows[-2]),'value':int(rows[-1])}) for rows in reader]

    return out