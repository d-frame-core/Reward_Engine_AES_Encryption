from Cryptodome.Protocol.KDF import PBKDF2
import mysql.connector
import base64, sys
from dotenv import load_dotenv
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Util.Padding import unpad
import os

load_dotenv()

AuroraDBhostCluster=os.getenv("AuroraDBhostCluster")
UsernameAuroraDB=os.getenv("UsernameAuroraDB")
PasswordAuroraDB=os.getenv("PasswordAuroraDB")
PortAuroraDB=os.getenv("PortAuroraDB")
DatabaseAuroraDB=os.getenv("DatabaseAuroraDB")

database=mysql.connector.connect(
    host=AuroraDBhostCluster,
    user=UsernameAuroraDB,
    password=PasswordAuroraDB,
    port=PortAuroraDB,
    database=DatabaseAuroraDB
)

# Useraddress of user
Address="0xA0D4594DC85b492dfAc756C6D4f6398e3a005767" 

cursorObject=database.cursor()

query="SELECT * FROM users where publicAddress='{}'".format(Address)

cursorObject.execute(query)

myresult=cursorObject.fetchall()

passwdkey_b64=myresult[0][1]
saltkey_b64=myresult[0][2]

print(saltkey_b64)
print(passwdkey_b64)

passwd_bytes = base64.b64decode(passwdkey_b64)
salt_bytes = base64.b64decode(saltkey_b64)

key = scrypt(passwd_bytes, salt_bytes, key_len=32, N=2**20, r=8, p=1)

with open("./userdata.bin", "rb") as file_in:
        tag_bytes = file_in.read(16)
        nonce_bytes = file_in.read(16)
        ciphertext_bytes = file_in.read()


AES_cipher_instance = AES.new(key, AES.MODE_GCM, nonce=nonce_bytes)

plaintext_bytes = unpad(AES_cipher_instance.decrypt_and_verify(ciphertext_bytes, tag_bytes), AES.block_size)

plaintext = plaintext_bytes.decode('utf-8')

print(plaintext)

sys.stdout.flush()