from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA512
import pymongo, base64
import os, bson, certifi
import schedule, time
import subprocess, sys
from web3 import Web3
from dotenv import load_dotenv
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Util.Padding import pad, unpad
from datetime import datetime
from datetime import date
import boto3
import redis

load_dotenv()

connectionString=os.getenv("ConnectionString")
contractAddress=os.getenv("Address")
ABI=os.getenv("ABI")
alchemyURL=os.getenv("AlchemyURL")
privateKey=os.getenv("PrivateKey")
publicAddress=os.getenv("PublicAddress")

ca = certifi.where()

def TransferToken():

        #The date should always be 1 because we are calling transferToken() function once a month to save gas fees
        if date.today().day != 1:
                return
        if(counter<=1):
                counter=counter+1
        web3=Web3(Web3.HTTPProvider(alchemyURL))
        contract=web3.eth.contract(address=contractAddress,abi=ABI)
        Wallet_from=Web3.to_checksum_address(publicAddress)
        Data=collection.find()
        for datas in Data:
                totalDft=round(datas["DFT"])
                SendingAddress=datas["useraddress"]
                Wallet_to=Web3.to_checksum_address(SendingAddress)
                nonce=web3.eth.get_transaction_count(Wallet_from)
                contract_txn=contract.functions.transfer(Wallet_to,totalDft*10**18,).build_transaction(
                    {
                        'chainId': 80001,
                        'nonce': nonce,
                        'gas': 100000,
                        'gasPrice': web3.to_wei("20", "gwei")
                    }
                )
                signed_tx=web3.eth.account.sign_transaction(contract_txn,privateKey)
                tx_hash=web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(web3.to_hex(tx_hash))
                collection.update_one({"useraddress":datas["useraddress"]},{"$inc":{"DFT":-datas["DFT"]}})
        


def EncryptData():

        score=score+1

        # Set your Redis password
        redis_password = "thisismynewpassword"
        # Connect to the Redis server with authentication

        # This client is for fetching encryption keys
        redis_client1 = redis.StrictRedis(host='localhost', port=6379, db=0, password=redis_password)
        # This client is for storing ipfs CID
        redis_client2 = redis.StrictRedis(host='localhost', port=6379, db=1, password=redis_password)
     
        def getEncryptionKey(userAddress):
                try:
                # Retrieving Encryption Key associated with the user_address
                        return redis_client1.zrange(userAddress, 0, -1)
                except redis.RedisError as e:
                        print(f"Error retrieving Encryption Key for {userAddress}: {e}")
                        return []

        Data=collection.find()
        for datas in Data:

                Address=datas["useraddress"]

                encryptionKeys=getEncryptionKey(Address)
                
                passwdkey_b64=encryptionKeys[0].decode()
                saltkey_b64=encryptionKeys[1].decode()

                data_bytes= datas.encode('UTF-8')


                passwd_bytes = base64.b64decode(passwdkey_b64)
                salt_bytes = base64.b64decode(saltkey_b64)
                nonce_bytes = os.urandom(16)

                key = scrypt(passwd_bytes, salt_bytes, key_len=32, N=2**20, r=8, p=1)

                AES_cipher_instance = AES.new(key, AES.MODE_GCM, nonce=nonce_bytes)

                ciphertext_bytes, tag_bytes = AES_cipher_instance.encrypt_and_digest(pad(data_bytes, AES.block_size))

                with open("userdata.bin", "wb") as file_out:
                        file_out.write(tag_bytes)
                        file_out.write(nonce_bytes)
                        file_out.write(ciphertext_bytes)

                #Calling ipfsScript in this Dir to write the encrypted data into Ipfs Node.
                p = subprocess.Popen(["node", "/Users/aryaa/Desktop/REWARDENGINESCRIPT/ipfsScript.js", sys.executable], stdout=subprocess.PIPE)
                out = p.stdout.read()
                CID=out.decode()

                print(CID)
                
                IPFS_CID=CID

                USER_PUBLIC_ADDRESS=Address

                #Putting Cid in redis-server
                try:
                # Add the ipfs_cid to the set associated with the user_address
                        redis_client2.zadd(USER_PUBLIC_ADDRESS, {IPFS_CID: score})
                        print(f"Added {IPFS_CID} for {USER_PUBLIC_ADDRESS}")
                except redis.RedisError as e:
                        print(f"Error adding {IPFS_CID} for {USER_PUBLIC_ADDRESS}: {e}")            
                
        redis_client1.quit()
        redis_client2.quit()


def readDocumments():
        
# Mongoose Schema for the MongoDb where the Data will come from Kafka look like(/.mongooseSchema).

# datashared field is used to set previously data shared by the the user, so that we can compare current data shared and previously data shared and
# give rewards to those user who actually shared the data.

# DFT field is used to set the total DFTs user got for the data they shared and will be transfered(DFT) once in a month using transferToken() function.

# userAddress field will have the wallet address of the user throught which they logged in

        if(counter==0):
                dftToBeShared=0.5
        elif(counter==1):
                dftToBeShared=0.25
        else: 
            dftToBeShared=0.125
        Data=collection.find()
        for datas in Data:
                DataSize=len(bson.BSON.encode(datas))*0.000001

                #notToBeCalculated is used so that the variables that will remain always in the mongoDB should not be included while
                #calulating the size of the data user shared 
                notToBeCalculated=len(bson.BSON.encode({"datashared":datas["datashared"], "useraddress":datas["useraddress"], "DFT":datas["DFT"]}))*0.000001
                if((DataSize-notToBeCalculated)>datas["datashared"]):
                        collection.update_one({"useraddress":datas["useraddress"]},{"$inc":{"DFT":dftToBeShared}})
                        collection.update_one({"useraddress":datas["useraddress"]},{"$set":{"datashared":DataSize-notToBeCalculated}})


if __name__ == "__main__":
    client = pymongo.MongoClient(connectionString,tlsCAFile=ca)
    db = client["analytics-layer"] #Database name in mongogDB
    collection = db["analytics-data"] #Collection name inside database name in mongogDB
    print(collection)
    counter=0 #Counter is for counting the number of times the transferToken() function will be triggered
    score=0 #For calculating score of adding IPFS CID in redis sorted set, IPFS CID stored with less score will be on top than CID stored with high score.
 

#Schedule is used for automating the Script
#Each function will be triggered at specific interval of time
schedule.every().day.at("00:00").do(readDocumments)
schedule.every().monday.at('18:00').do(EncryptData)
schedule.every().day.at("09:00").do(TransferToken)

while 1:
        schedule.run_pending()
        time.sleep(1)   
