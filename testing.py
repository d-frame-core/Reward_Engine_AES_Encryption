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
print("Divyyesh Not here")


a=7
print(bytes(a))
ca = certifi.where()
listArray=[0,"hellonkfnvfjknvfjkbnf"]

dict={
'id':'crannells0',
'mac_address':
'D3-44-4C-C1-B1-14'
}
dict1={
"id":"crannells0",
"mac_address":
"D3-44-4C-C1-B1-14"
}
Data=len((bson.BSON.encode(dict)))
Data1=len((bson.BSON.encode(dict1)))
print(Data)
print(Data1)

def readDocumments():

        Data=len(bson.BSON.encode({"datashared":datas["datashared"]}))
        print("Working Fine")
        for documents in collections:
            Data=db[documents].find()
            for datas in Data:
                print(datas["age"])
        # web3=Web3(Web3.HTTPProvider(alchemyURL))
        # contract=web3.eth.contract(address=contractAddress,abi=ABI)
        # DFTsymbol=contract.functions.symbol().call()
        # print(DFTsymbol)


if __name__ == '__main__':
    print("Divyyesh Here")
    client = pymongo.MongoClient(connectionString,tlsCAFile=ca)
    db = client['analytics-layer']
    collections = db.list_collection_names()
    print(collections)
    # readDocumments()


# schedule.every(1).minutes.do(readDocumments)
# schedule.every().saturday.at('18:44').do(readDocumments)
# while 1:
#         schedule.run_pending()
#         time.sleep(1)        

             





