import base64, os
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Util.Padding import pad, unpad


# data = '''A large percentage in all areas (software engineering, network engineering, system administration, database administration, you name it) were both very good technically and very practical at the same time, which led them to understand real-world security risks and considerations (starting with Max Levchin who was deeply versed in math and cryptography). Employees who were intimately involved with live site support and operations were universally top-notch and extremely dedicated and would considering any security breach a personal affront, so they did everything possible to guard against it was a lot easier to have developers'''


# data_bytes = data.encode('UTF-8')


# passwdkey_b64 = "R15M44oRjYaJP+RQmT53E9Nlz9SBQL1HaAKefOt+9Ws="
# saltkey_b64 = "5evW1aCyDNX6red6Lf0B8KvpnTgdfDZN8pbnQNh1ua8="


# passwd_bytes = base64.b64decode(passwdkey_b64)
# salt_bytes = base64.b64decode(saltkey_b64)
# nonce_bytes = os.urandom(16)


# key = scrypt(passwd_bytes, salt_bytes, key_len=32, N=2**20, r=8, p=1)

# AES_cipher_instance = AES.new(key, AES.MODE_GCM, nonce=nonce_bytes)

# ciphertext_bytes, tag_bytes = AES_cipher_instance.encrypt_and_digest(pad(data_bytes, AES.block_size))

# with open("userdata.bin", "wb") as file_out:
#     file_out.write(tag_bytes)
#     file_out.write(nonce_bytes)
#     file_out.write(ciphertext_bytes)



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


plaintext = plaintext_bytes.decode('utf-8')

print(plaintext)