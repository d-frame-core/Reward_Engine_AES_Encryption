from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA512
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
from datetime import datetime
from datetime import date
import boto3
import json

load_dotenv()

AuroraDBhostCluster=os.getenv("AuroraDBhostCluster")
UsernameAuroraDB=os.getenv("UsernameAuroraDB")
PasswordAuroraDB=os.getenv("PasswordAuroraDB")
PortAuroraDB=os.getenv("PortAuroraDB")
DatabaseAuroraDB=os.getenv("DatabaseAuroraDB")
# import boto3

datas={
  "id":"divyyesh",
  "mac_address":"D3-44-4C-C1-B14",
  "ip_address":"108.102.333333",
  "longitude":126.9826111,
  "id":"divyyesh",
  "mac_address":"D3-44-4C-C1-B14",
  "ip_address":"108.102.333333",
  "longitude":126.9826111,
}

database=mysql.connector.connect(
    host=AuroraDBhostCluster,
    user=UsernameAuroraDB,
    password=PasswordAuroraDB,
    port=PortAuroraDB,
    database=DatabaseAuroraDB
)

Address="0xA0D4594DC85b492dfAc756C6D4f6398e3a005767"

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

table = dynamodb.Table("IPFS_USER-CID")

cursorObject=database.cursor()

query="SELECT * FROM users where publicAddress='{}'".format(Address)

cursorObject.execute(query)

myresult=cursorObject.fetchall()

passwdkey_b64=myresult[0][1]
saltkey_b64=myresult[0][2]

datas=json.dumps(datas)

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

p = subprocess.Popen(["node", "/Users/aryaa/OneDrive/Desktop/RewardScript/ipfsScript.js", sys.executable], stdout=subprocess.PIPE)

out = p.stdout.read()

CID=out.decode()

print(CID)

IPFS_CID=CID

USER_PUBLIC_ADDRESS=Address

try:
    output = table.put_item(
        Item={
                "UserPublicAddress": USER_PUBLIC_ADDRESS,
                "DeployedDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"),
                "IpfsCid": IPFS_CID
        }
    )

    status_code = output["ResponseMetadata"]["HTTPStatusCode"]
    if(status_code == 200):
        print("Record entered to DynamoDB successfully")
    else:
        print("Error Occur During Record Insertion")

except Exception as e:
        print(f"An error occurred: {str(e)}")

database.close()


