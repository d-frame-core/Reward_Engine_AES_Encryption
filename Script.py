import pymongo
from dotenv import load_dotenv
import os, bson, certifi
import schedule, time
from web3 import Web3

load_dotenv()

connectionString=os.getenv("ConnectionString")
contractAddress=os.getenv("Address")
ABI=os.getenv("ABI")
alchemyURL=os.getenv("AlchemyURL")

ca = certifi.where()

def TransferToken():
        
        if(counter<=11):
                counter=counter+1
        web3=Web3(Web3.HTTPProvider(alchemyURL))
        contract=web3.eth.contract(address=contractAddress,abi=ABI)
        Data=collection.find()
        for datas in Data:
                totalDft=datas["DFT"]
                Address=datas["useraddress"]
                contract.functions.transfer(Address,totalDft).call()
                collection.update_one({"useraddress":datas["useraddress"]},{"$inc":{"DFT":-datas["DFT"]}})


def readDocumments():

        if(counter>=4 and counter<=7):
                dftToBeShared=0.25/4
        elif(counter>=8 and counter<=11):
                dftToBeShared=0.125/4
        Data=collection.find()
        for datas in Data:
                DataSize=len(bson.BSON.encode(datas))*0.000001
                notToBeCalculated=len(bson.BSON.encode({"datashared":datas["datashared"], "useraddress":datas["useraddress"], "DFT":datas["DFT"]}))*0.000001
                if((DataSize-notToBeCalculated)>datas["datashared"]):
                        collection.update_one({"useraddress":datas["useraddress"]},{"$inc":{"DFT":dftToBeShared}})
                        collection.update_one({"useraddress":datas["useraddress"]},{"$set":{"datashared":DataSize}})


if __name__ == "__main__":
    client = pymongo.MongoClient(connectionString,tlsCAFile=ca)
    db = client["analytics-layer"]
    collection = db["analytics-data"]
    dftToBeShared=0.5/4
    counter=0


schedule.every(6).hours.do(readDocumments)
schedule.every().monday.at('21:00').do(TransferToken)
while 1:
        schedule.run_pending()
        time.sleep(1)        

             





