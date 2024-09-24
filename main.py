from typing import List
from DataBaseClient import StarDataBaseClient
from Visualisation import Visualisation
from Star import Star
import os


def createTables():
    db.createIdTable()
    db.createHeaderTable(listStar[0].header)
    db.createDataTable()
    db.createTypeTable()
    db.createPreCalcDataTable()

def fillTables():
    index = 1
    for star in listStar:
        db.insertIdTable(index)
        db.insetrIntoHeaderTable(star.header, index)
        db.insertIntoDataTable(star.data, index)
        db.insertType(star.smallType, star.bigType, index)
        index += 1
    
    for i in range(1, len(listStar)):
        db.insertPrecalcData(i)

def sqlSelectGreatWaveLength(db:StarDataBaseClient):
    sqlc = '''SELECT id 
    FROM SpectrumPreCalculateData
    WHERE max_wavelength > 5 AND min_wavelength < 0.81'''
    db.cursor.execute(sqlc)
    print(db.cursor.fetchall())


def sqlCount(type: str):
    sqlc='''SELECT COUNT(shortType)
    FROM SpectrumType
    WHERE shortType like '%''' + type + "%';"
    db.cursor.execute(sqlc)
    return db.cursor.fetchall()[0][0]

def sqlAVG():
    sqla = '''SELECT AVG(min_fluxdensity)
    FROM SpectrumPreCalculateData'''
    db.cursor.execute(sqla)
    return db.cursor.fetchall()[0][0]

def sqlSum():
    sqls = '''SELECT SUM(min_fluxdensity)
    FROM SpectrumPreCalculateData'''
    db.cursor.execute(sqls)
    return db.cursor.fetchall()[0][0]

def getCountsOfType(types: List[str]) -> List[int]:
    counts = []
    for tp in  types:
        counts.append(sqlCount(tp))
    return counts
     
def getSomeXandYData(db: StarDataBaseClient, lst: List[int]):
    listsOfCoord = []
    listOfTypes = []
    for item in lst:
        listsOfCoord.append(db.getDataTableItem(item))
        listOfTypes.append(db.getElement("SpectrumType", "shortType", item))
    return (listsOfCoord, listOfTypes)
        


fileNames = os.listdir("resources")
listStar = []

for fileName in fileNames:
    uri = 'resources/' + fileName
    listStar.append(Star(uri))

db = StarDataBaseClient()
db.connectDB()

#createTables()
#fillTables()

print(sqlCount('K'))
print(sqlAVG())
print(sqlSum())

sqlSelectGreatWaveLength(db)
data = db.getDataTableItem(2)
#Visualisation.chartSpectrum(data[0], data[1])
#Visualisation.colormapAndXY(data[0], data[1])
types = ['G', 'K', 'M', 'S', 'T', 'L', 'C', 'F']
#Visualisation.typeBar(types, getCountsOfType(types))

coords = getSomeXandYData(db, [26, 93, 122, 1])
Visualisation.someSpectrumPlot(coords[0], coords[1])

db.disconnectDB()




