import json
import sqlite3
import numpy as np
import io

class StarDataBaseClient:
    def __init__(self) -> None:
        self._databaseKeys = []


    def connectDB(self):
        self._connection = sqlite3.connect('StarSpectrum.db')
        self.cursor = self._connection.cursor()

    def disconnectDB(self):
        self._connection.commit()
        self._connection.close()

    def adapt_array(self, arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def convert_array(self,text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    def createIdTable(self):
        sqlCreateIdTable = '''CREATE TABLE IF NOT EXISTS IdSpectrum (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        header_id INTEGER, 
        data_id INTEGER, 
        type_id INTEGER, 
        precalc_id INTEGER)'''
        self.cursor.execute(sqlCreateIdTable)
        self._connection.commit()
        
    def insertIdTable(self, id:int):
        sqlInsertIdTable = '''INSERT INTO IdSpectrum (header_id, data_id, type_id, precalc_id) VALUES (?, ?, ?, ?)'''
        self.cursor.execute(sqlInsertIdTable, (id, id, id, id))
        self._connection.commit()



    def createHeaderTable(self, headerDict:dict):
        sqlCreateDatabase = '''CREATE TABLE IF NOT EXISTS SpectrumHeader (
        id INTEGER, '''
        self._databaseKeys

        for k,v in headerDict.items():
            if k != "COMMENT":
                
                self._databaseKeys.append(k)
                sqlCreateDatabase += k.lower() + " "
                if isinstance(v,float):
                    sqlCreateDatabase += "REAL"
                if isinstance(v,int):
                    sqlCreateDatabase += "INTEGER"
                if isinstance(v, str):
                    sqlCreateDatabase += "TEXT"
                sqlCreateDatabase += ', '
        sqlCreateDatabase = sqlCreateDatabase[:-2] + ')'

        self.cursor.execute(sqlCreateDatabase)
        self._connection.commit()

    def insetrIntoHeaderTable(self, headerDict:dict, id:int):
        sqlAddItemKeys = "INSERT INTO SpectrumHeader (id, "
        for k in self._databaseKeys:
            sqlAddItemKeys += k
            sqlAddItemKeys += ", "

        sqlAddItemKeys = sqlAddItemKeys[:-2]

        sqlAddItemKeys += ") VALUES ("
        for k in self._databaseKeys:     
            sqlAddItemKeys += '?, '
        sqlAddItemKeys = sqlAddItemKeys + '?)'

        sqlAddItemItems = [id]
        for k  in self._databaseKeys:
            if k != "COMMENT":
                if k in headerDict:
                    sqlAddItemItems.append(headerDict[k])
                else: sqlAddItemItems.append(None)

        self.cursor.execute(sqlAddItemKeys, sqlAddItemItems)
        self._connection.commit()

    def getDataTableItem(self, id:int):
        sqlGetDataTable = '''SELECT wavelength, fluxdensity FROM SpectrumData
                                WHERE id='''+id.__str__()
        self.cursor.execute(sqlGetDataTable)
        data = self.cursor.fetchall() 

        X = self.convert_array(data[0][0])
        Y = self.convert_array(data[0][1])
 
        return (X, Y)
    
    def getDataTableItemError(self, id:int):
        sqlGetDataTable = '''SELECT error FROM SpectrumData
                                WHERE id='''+id.__str__()
        self.cursor.execute(sqlGetDataTable)
        data = self.cursor.fetchall() 
        Error = self.convert_array(data[0][0])
        return Error

    def createDataTable(self):
        sqlAddDataTable = '''CREATE TABLE IF NOT EXISTS SpectrumData (
        id INTEGER,
        wavelength BLOB,
        fluxdensity BLOB,
        error BLOB
        );'''
        self.cursor.execute(sqlAddDataTable)
        self._connection.commit()

    def insertIntoDataTable(self, data, id:int):
        sqlAddDataItems ='''INSERT INTO SpectrumData (id, wavelength, fluxdensity, error) VALUES (?, ?, ?, ?)'''
        
        binDataList = [id]
        for d in data:
            binDataList.append(self.adapt_array(d))

        self.cursor.execute(sqlAddDataItems, binDataList)
        self._connection.commit()

    def createTypeTable(self):
        sqlCreateTypeTable = '''CREATE TABLE IF NOT EXISTS SpectrumType (
        id INTEGER,
        shortType TEXT,
        longType TEXT
        );'''
        self.cursor.execute(sqlCreateTypeTable)

    def insertType(self, shortType, longType, id:int):
        sqlCreateTypeTable = "INSERT INTO SpectrumType (id, shortType, longType) VALUES (?, ?, ?)"
        self.cursor.execute(sqlCreateTypeTable, (id, shortType, longType))
        self._connection.commit()   

    def getAllTypes(self):
        sqlgetTypes = '''SELECT shortType FROM SpectrumType'''   
        self.cursor.execute(sqlgetTypes)
        return self.cursor.fetchall()

    def getElement(self, table: str, field: str, id: int):
        sqlel = "SELECT " + field + " FROM " + table + " WHERE id=" + id.__str__()
        self.cursor.execute(sqlel)
        return self.cursor.fetchall()[0][0]

    def createPreCalcDataTable(self):
        sqlCreatePreCalcDataTable ='''
        CREATE TABLE IF NOT EXISTS SpectrumPreCalculateData (
        id INTEGER,
        min_wavelength REAL,
        max_wavelength REAL,
        average_wavelength REAL,
        median_wavelength REAL,
        min_fluxdensity REAL,
        max_fluxdensity REAL,
        average_fluxdensity REAL,
        median_fluxdensity REAL,  
        min_error REAL,
        max_error REAL,
        average_error REAL,
        median_error REAL)
        '''
        self.cursor.execute(sqlCreatePreCalcDataTable)
        self._connection.commit()

    def insertPrecalcData(self, id:int):
        self.cursor.execute('''SELECT * FROM SpectrumData
                                WHERE id='''+id.__str__())
                         
        data = self.cursor.fetchall()      
        X = self.convert_array(data[0][1])
        Y = self.convert_array(data[0][2])
        Error = self.convert_array(data[0][3]) 

        calcdataX = self.__getCalcData(X)
        calcdataY = self.__getCalcData(Y)
        calcdataError = self.__getCalcData(Error)
        
        sqlInsertPrecalcData= '''INSERT INTO SpectrumPreCalculateData (
        id,
        min_wavelength, 
        max_wavelength, 
        average_wavelength, 
        median_wavelength,
        min_fluxdensity,
        max_fluxdensity,
        average_fluxdensity,
        median_fluxdensity, 
        min_error,
        max_error,
        average_error,
        median_error) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        self.cursor.execute(sqlInsertPrecalcData, (id,) + calcdataX + calcdataY + calcdataError)
        self._connection.commit()



    def __getCalcData(self, list):
        return (float(min(list)), float(max(list)), float(self.__average(list)), float(self.__median(list)))

    def __median(self, list) -> float:    
        sortedList = sorted(list)
        midx = (sortedList.__len__() - 1) // 2

        if sortedList.__len__() % 2 == 0: 
            return (sortedList[midx] + sortedList[midx + 1]) / 2.0
        else:  
            return sortedList[midx]
    
    def __average(self, list) -> float:       
        sum = 0
        for item in list:
            if np.isnan(item) == False:
                sum += item
        return sum/len(list)

