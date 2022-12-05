from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
# from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Hash import SHA512

data = '''A large percentage of early technical employees in all areas (software engineering, network engineering, system administration, database administration, you name it) were both very good technically and very practical at the same time, which led them to understand real-world security risks and considerations (starting with Max Levchin who was deeply versed in math and cryptography).
Employees who were intimately involved with live site support and operations were universally top-notch and extremely dedicated and would consider any security breach a personal affront, so they did everything possible to guard against it (NB: it was a lot easier to have developers be involved in live site support before SOX [1]).
While the team had cut plenty of corners in feature development and the codebase was far from perfect, when it came to security infrastructure the standards were extremely high (another example of practicality that was a universal trait of the vast majority of early PayPal'ers).
I vividly remember one of the first new concepts I learned after joining - that of a "share party": at the time restarting live services after maintenance or outages required simultaneous involvement of 3 out of 8 trusted "shareholders" who jointly held the keys to the secrets (encryption keys etc) that were required for the system to operate [2]'''

bytedata = data.encode('UTF-8')
# print(bytedata)

key16 = 'c80667c845f47d0a5351e67ef968bcb9'
key32 = "6b5c8247110a6dc685a1a25c01f28b0d47bd0d5b36456b5242e801ebcb4c5a67"
salt = bytes.fromhex(key16)

key = PBKDF2(key32, salt, 32, count=100000, hmac_hash_module=SHA512)

print(key)

cipherkey = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipherkey.encrypt_and_digest(bytedata)

print(ciphertext, tag)

file_out = open("encrypted.bin", "wb")
[ file_out.write(x) for x in (cipherkey.nonce, tag, ciphertext) ]
file_out.close()

# Decryption Part

file_in = open("encrypted.bin", "rb")
nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]

cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)
print(data)
