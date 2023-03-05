import pymongo, base64
import os, bson, certifi
import schedule, time
import subprocess, sys
from web3 import Web3
from dotenv import load_dotenv
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
# from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Hash import SHA512
import subprocess
import sys

load_dotenv()

connectionString=os.getenv("ConnectionString")
contractAddress=os.getenv("Address")
ABI=os.getenv("ABI")
alchemyURL=os.getenv("AlchemyURL")

IPFS_CID=""
USER_PUBLIC_ADDRESS=""

ca = certifi.where()

def TransferToken():
        
        if(counter<=11):
                counter=counter+1
        web3=Web3(Web3.HTTPProvider(alchemyURL))
        contract=web3.eth.contract(address=contractAddress,abi=ABI)
        database=mysql.connector.connect(
                host="DB_ENDPOINT",
                user= "admin",
                password="<DB_PASSWORD>",
                port= 3302,
                database="myDB"
        )
        Data=collection.find()
        for datas in Data:

                totalDft=datas["DFT"]
                Address=datas["useraddress"]
                contract.functions.transfer(Address,totalDft).call()

                bytedata = datas.encode('UTF-8')
                # print(bytedata)

                key16 = 'c80667c845f47d0a5351e67ef968bcb9'
                key32 = "6b5c8247110a6dc685a1a25c01f28b0d47bd0d5b36456b5242e801ebcb4c5a67"
                salt = bytes.fromhex(key16)

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

                p = subprocess.Popen(["node", "/Users/aryaa/Desktop/REWARDENGINESCRIPT/ipfsScript.js", sys.executable], stdout=subprocess.PIPE)
                out = p.stdout.read()
                CID=out.decode()

                IPFS_CID=CID
                print(CID)

                # Decryption Part

                passwdkey_b64 = "R15M44oRjYaJP+RQmT53E9Nlz9SBQL1HaAKefOt+9Ws="
                saltkey_b64 = "5evW1aCyDNX6red6Lf0B8KvpnTgdfDZN8pbnQNh1ua8="

                passwd_bytes = base64.b64decode(passwdkey_b64)
                salt_bytes = base64.b64decode(saltkey_b64)


                key = scrypt(passwd_bytes, salt_bytes, key_len=32, N=2**20, r=8, p=1)


                with open("userdata.bin", "rb") as file_in:
                        tag_bytes = file_in.read(16)
                        nonce_bytes = file_in.read(16)
                        ciphertext_bytes = file_in.read()


                AES_cipher_instance = AES.new(key, AES.MODE_GCM, nonce=nonce_bytes)

                plaintext_bytes = unpad(AES_cipher_instance.decrypt_and_verify(ciphertext_bytes, tag_bytes), AES.block_size)

                cipher = AES.new(key, AES.MODE_EAX, nonce)
                data = cipher.decrypt_and_verify(ciphertext, tag)
                print(data)
                
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


schedule.every().day.at("00:00").do(readDocumments)
schedule.every().monday.at('21:00').do(TransferToken)
while 1:
        schedule.run_pending()
        time.sleep(1)   



# QLDB Script From Here  

retry_config = RetryConfig(retry_limit=3)

print("Initializing the driver")

qldb_driver = QldbDriver("IPFSCIDLedger", retry_config=retry_config)

def insert_documents(transaction_executor, aws_ion):
    print("Inserting a document into IPFSCIDLedger")
    transaction_executor.execute_statement(f"INSERT INTO USER_ADDRESS_IPFS_CID ?", aws_ion)

IPFS_CID="xq5xfqxvqtfy44422"

USER_PUBLIC_ADDRESS="xfyatsfxafx7755"

user_meta_data = { 
            'CID': IPFS_CID,
            'DATE': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'User_Public_Address': USER_PUBLIC_ADDRESS
          }

qldb_driver.execute_lambda(lambda x: insert_documents(x, user_meta_data))

print(f"Document with CID ${IPFS_CID} Inserted to USER_ADDRESS_IPFS_CID Table")