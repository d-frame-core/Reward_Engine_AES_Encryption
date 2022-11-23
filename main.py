from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

data = '''A large percentage of early technical employees in all areas (software engineering, network engineering, system administration, database administration, you name it) were both very good technically and very practical at the same time, which led them to understand real-world security risks and considerations (starting with Max Levchin who was deeply versed in math and cryptography).
Employees who were intimately involved with live site support and operations were universally top-notch and extremely dedicated and would consider any security breach a personal affront, so they did everything possible to guard against it (NB: it was a lot easier to have developers be involved in live site support before SOX [1]).
While the team had cut plenty of corners in feature development and the codebase was far from perfect, when it came to security infrastructure the standards were extremely high (another example of practicality that was a universal trait of the vast majority of early PayPal'ers).
I vividly remember one of the first new concepts I learned after joining - that of a "share party": at the time restarting live services after maintenance or outages required simultaneous involvement of 3 out of 8 trusted "shareholders" who jointly held the keys to the secrets (encryption keys etc) that were required for the system to operate [2]'''

bytedata = data.encode('UTF-8')
print(bytedata)

Key = get_random_bytes(32)
print(Key)

cipherkey = AES.new(Key, AES.MODE_EAX)
ciphertext, tag = cipherkey.encrypt_and_digest(bytedata)

print(ciphertext, tag)

file_out = open("encrypted.bin", "wb")
[ file_out.write(x) for x in (cipherkey.nonce, tag, ciphertext) ]
file_out.close()
