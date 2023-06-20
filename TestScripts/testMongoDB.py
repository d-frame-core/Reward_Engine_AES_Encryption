import pymongo
from dotenv import load_dotenv
import os, bson, certifi

load_dotenv()

connectionString=os.getenv("ConnectionString")
# contractAddress=os.getenv("Address")
# ABI=os.getenv("ABI")
# alchemyURL=os.getenv("AlchemyURL")
print("Divyyesh Not here")


ca = certifi.where()
listArray=[0,"hellonkfnvfjknvfjkbnf"]

dict={
'id':'crannells0',
'mac_address':'D3-44-4C-C1-B1-14',
'website':{
     'sports':{
     'cricbuzz':['https://www.sportskeeda.com/','https://www.sportskeeda.com/'],
     'ESPN':['https://www.espn.in/','https://www.espn.in/','https://www.sportskeeda.com/']
     }
 }
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

        # Data=len(bson.BSON.encode({"datashared":datas["datashared"]}))
        # print("Working Fine")
        for collection in collections:
            Data=db[collection].find()
            sum=0
            for datas in Data:
                print(datas)
                sum=sum+len(bson.BSON.encode(datas))*0.000001
            print(sum)
            # for datas in Data:
            #     print(datas["age"])
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
    readDocumments()


# schedule.every(1).minutes.do(readDocumments)
# schedule.every().saturday.at('18:44').do(readDocumments)
# while 1:
#         schedule.run_pending()
#         time.sleep(1)        

             





