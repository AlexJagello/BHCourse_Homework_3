from astropy.io import fits
import pandas as pd
import numpy as np
import os


class Star:
    def __init__(self, path):
        self.data = fits.getdata(path)
        self.header =self.__changeKeys(fits.getheader(path))
        self.smallType = self.__smallType(path)
        self.bigType = self.__bigType(path)
        self.X = self.data[0]
        self.Y = self.data[1]
        self.Errors = self.data[2]
    
    def __changeKeys(self, dictionary:dict) -> dict:
        newDict = {}
        for k,v in dictionary.items():
            newKey = k.replace('(','').replace(')', '').replace('-','_')
            newDict.update({newKey: v})
        return newDict

    def __smallType(self, path:str) -> str:
        slashSignIndex = path.find('/')
        return path[slashSignIndex+1: slashSignIndex + 3].strip('-')

    def __bigType(sel, path:str) -> str:
        slashSignIndex = path.find('/')
        filename = path[slashSignIndex+1: ]
        underscoreSignIndex = filename.find('_')
        if underscoreSignIndex != -1:
           return filename[: underscoreSignIndex]      
        return "unknown"
    


if __name__ == '__main__':
    fileNames = os.listdir("resources")
    listStar = []

    for fileName in fileNames:
        uri = 'resources/' + fileName

        listStar.append(Star(uri))


    infoDF= pd.DataFrame(
    {
        "min y" : [y.minY for y in listStar],
        "max y" : [y.maxY for y in listStar],
        "med y" : [y.medianY for y in listStar],
        "avr y" : [y.averageY for y in listStar],
        "smalltype" : [y.smallType for y in listStar],
        "type" : [y.bigType for y in listStar]
     })


    print(infoDF.head(50))