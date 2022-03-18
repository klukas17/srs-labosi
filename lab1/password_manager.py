#!/usr/bin/env python3

# pokreni chmod +x test.py

from pydoc import plain
from sys import argv
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Cipher import AES

SALT_UPPER_BOUND = 32 # len = 32
NONCE_UPPER_BOUND = 44 # len = 12
TAG_UPPER_BOUND = 60 # len = 16

def verify_args():
    if len(argv) <= 1:
        print("Missing arguments! First argument can be init, put, get.")
        exit(1)
    elif argv[1] == "init":
        if len(argv) != 3:
            print("Wrong arguments! Arguments for the init command must be in 'init {master_password}' format.")
            exit(1)
    elif argv[1] == "put":
        if len(argv) != 5:
            print("Wrong arguments! Arguments for the put command must be in 'put {master_password} {address} {password}' format.")
            exit(1)
    elif argv[1] == "get":
        if len(argv) != 4:
            print("Wrong arguments! Arguments for the put command must be in 'get {master_password} {address}' format.")
            exit(1)
    else:
        print("Wrong arguments! First argument can be init, put, get.")
        exit(1)

def write(master_password, data):
    f = open('vault', 'wb')

    salt = get_random_bytes(32)
    key = PBKDF2(password=master_password, salt=salt, dkLen=32, count=1000000, hmac_hash_module=SHA512) 
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    f.write(salt + nonce + tag + ciphertext)
    f.close()

def init():
    write(master_password=argv[2], data=b"Password manager")
    print("Password manager initialized.")

def check():
    master_password = argv[2]

    f = open('vault', 'rb')
    d = f.read()
    salt = d[:SALT_UPPER_BOUND]
    nonce = d[SALT_UPPER_BOUND:NONCE_UPPER_BOUND]
    tag = d[NONCE_UPPER_BOUND:TAG_UPPER_BOUND]
    ciphertext = d[TAG_UPPER_BOUND:]

    try:
        key = PBKDF2(password=master_password, salt=salt, dkLen=32, count=1000000, hmac_hash_module=SHA512) 
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plain_text = cipher.decrypt_and_verify(ciphertext, tag)
        records = plain_text.decode('utf-8').split('\n')[1:]
        password_dictionary = {}
        for record in records:
            site, pas = record.split(' ')
            password_dictionary[site] = pas
        return password_dictionary
    except (ValueError, KeyError):
        print("Master password incorrect or integrity check failed.")
        exit(1)

def put():
    password_dictionary = check()
    address = argv[3]
    password = argv[4]

    password_dictionary[address] = password
    text = "Password manager"
    for site in password_dictionary:
        text += f'\n{site} {password_dictionary[site]}'
    write(master_password=argv[2], data=str.encode(text))

    print(f'Stored password for {address}.')
    
    
def get():
    password_dictionary = check()
    address = argv[3]

    try:
        password = password_dictionary[address]
        print(f'Password for {address} is: {password}.')
    except KeyError:
        print(f'Password for {address} was never saved.')

if __name__ == "__main__":
    verify_args()
    if argv[1] == "init":
        init()
    elif argv[1] == "put":
        put()
    elif argv[1] == "get":
        get()