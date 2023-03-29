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
import mysql.connector
import pymongo, base64
import os, bson, certifi
import schedule, time
import subprocess, sys
from web3 import Web3
from dotenv import load_dotenv
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Util.Padding import pad, unpad
from pyqldb.config.retry_config import RetryConfig
from pyqldb.driver.qldb_driver import QldbDriver
from datetime import datetime
from datetime import date
import boto3

load_dotenv()

connectionString=os.getenv("ConnectionString")
contractAddress=os.getenv("Address")
ABI=os.getenv("ABI")
alchemyURL=os.getenv("AlchemyURL")
privateKey=os.getenv("PrivateKey")
publicAddress=os.getenv("PublicAddress")


ca = certifi.where()


def insert_documents(transaction_executor, aws_ion):
    print("Inserting a document into IPFSCIDLedger")
    transaction_executor.execute_statement(f"INSERT INTO USER_ADDRESS_IPFS_CID ?", aws_ion)


def TransferToken():
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
        
        database=mysql.connector.connect(
                host="DB_ENDPOINT",
                user= "admin",
                password="<DB_PASSWORD>",
                port= 3302,
                database="myDB"
        )
        retry_config = RetryConfig(retry_limit=3)
        qldb_driver = QldbDriver("IPFSCIDLedger", retry_config=retry_config)
        Data=collection.find()
        for datas in Data:

                Address=datas["useraddress"]
                
                cursorObject=database.cursor()
                
                query="SELECT * FROM users where publicAddress='{}'".format(Address)
                
                cursorObject.execute(query)
                
                myresult=cursorObject.fetchall()

                passwdkey_b64=myresult[0][1]
                saltkey_b64=myresult[0][2]

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

                p = subprocess.Popen(["node", "/Users/aryaa/Desktop/REWARDENGINESCRIPT/ipfsScript.js", sys.executable], stdout=subprocess.PIPE)
                out = p.stdout.read()
                CID=out.decode()

                print(CID)
                
                IPFS_CID=CID

                USER_PUBLIC_ADDRESS=Address

                user_meta_data = { 
                        'CID': IPFS_CID,
                        'DATE': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        'User_Public_Address': USER_PUBLIC_ADDRESS
                }

                qldb_driver.execute_lambda(lambda x: insert_documents(x, user_meta_data))

                print(f"Document with CID ${IPFS_CID} Inserted to USER_ADDRESS_IPFS_CID Table")


                # Decryption Part

                # passwdkey_b64 = "R15M44oRjYaJP+RQmT53E9Nlz9SBQL1HaAKefOt+9Ws="
                # saltkey_b64 = "5evW1aCyDNX6red6Lf0B8KvpnTgdfDZN8pbnQNh1ua8="

                # passwd_bytes = base64.b64decode(passwdkey_b64)
                # salt_bytes = base64.b64decode(saltkey_b64)


                # key = scrypt(passwd_bytes, salt_bytes, key_len=32, N=2**20, r=8, p=1)


                # with open("userdata.bin", "rb") as file_in:
                #         tag_bytes = file_in.read(16)
                #         nonce_bytes = file_in.read(16)
                #         ciphertext_bytes = file_in.read()


                # AES_cipher_instance = AES.new(key, AES.MODE_GCM, nonce=nonce_bytes)

                # plaintext_bytes = unpad(AES_cipher_instance.decrypt_and_verify(ciphertext_bytes, tag_bytes), AES.block_size)
                
                # plaintext = plaintext_bytes.decode('utf-8')

                # print(plaintext)
                
        database.close()


def readDocumments():

        if(counter==0):
                dftToBeShared=0.5
        elif(counter==1):
                dftToBeShared=0.25
        else: 
            dftToBeShared=0.125
        Data=collection.find()
        for datas in Data:
                DataSize=len(bson.BSON.encode(datas))*0.000001
                notToBeCalculated=len(bson.BSON.encode({"datashared":datas["datashared"], "useraddress":datas["useraddress"], "DFT":datas["DFT"]}))*0.000001
                if((DataSize-notToBeCalculated)>datas["datashared"]):
                        collection.update_one({"useraddress":datas["useraddress"]},{"$inc":{"DFT":dftToBeShared}})
                        collection.update_one({"useraddress":datas["useraddress"]},{"$set":{"datashared":DataSize-notToBeCalculated}})


if __name__ == "__main__":
    client = pymongo.MongoClient(connectionString,tlsCAFile=ca)
    db = client["analytics-layer"]
    collection = db["analytics-data"]
    counter=0


schedule.every().day.at("00:00").do(readDocumments)
schedule.every().monday.at('18:00').do(EncryptData)
schedule.every().day.at("09:00").do(TransferToken)

while 1:
        schedule.run_pending()
        time.sleep(1)   

# DynamoDB Records Entry Script 

def put_item():
    dynamodb_instance = boto3.resource("dynamodb")
    table = dynamodb_instance.Table("IPFS_USER-CID")

    try:
        output = table.put_item(
            Item={
                "UserPublicAddress": "0xsgduygsdbhsdgbs",
                "DeployedDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"),
                "IpfsCID": "0vfrwfccwfvwfcxwgfcxwggvfwc"
            }
        )

        status_code = output["ResponseMetadata"]["HTTPStatusCode"]

        if(status_code == 200):
            print("Record entered to DynamoDB successfully")
        else:
            print("Error Occur During Record Insertion")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

put_item()