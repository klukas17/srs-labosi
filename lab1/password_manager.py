#!/usr/bin/env python3

from sys import argv
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES

SALT_UPPER_BOUND = 32 # len = 32
NONCE_UPPER_BOUND = 44 # len = 12
TAG_UPPER_BOUND = 60 # len = 16

SPACES = 4

def verify_args():
    if len(argv) <= 1:
        print("Missing arguments! First argument can be init, put, get.")
        exit(1)
    elif argv[1] == "help":
        if len(argv) != 2:
            print("Wrong arguments! Arguments for the help command must be in 'help' format.")
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
    elif argv[1] == "count":
        if len(argv) != 3:
            print("Wrong arguments! Arguments for the count command must be in 'count {master_password}' format.")
            exit(1)
    elif argv[1] == "list":
        if len(argv) != 3:
            print("Wrong arguments! Arguments for the list command must be in 'list {master_password}' format.")
            exit(1)
    else:
        print("Wrong arguments! First argument can be init, put, get.")
        exit(1)

def write(master_password, data):
    f = open('vault', 'wb')

    salt = get_random_bytes(32)
    key = scrypt(master_password, salt, 16, N=2**18, r=8, p=1)
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    f.write(salt + nonce + tag + ciphertext)
    f.close()

def help():
    print("Hello! Supported operations are:")
    print()
    print(f"{SPACES * ' '}init {{master_password}}")
    print(f"{SPACES * 2 * ' '}initialize and set the master password")
    print()
    print(f"{SPACES * ' '}put {{master_password}} {{address}} {{password}}")
    print(f"{SPACES * 2 * ' '}add a new record")
    print()
    print(f"{SPACES * ' '}get {{master_password}} {{address}}")
    print(f"{SPACES * 2 * ' '}fetch password for the specified address")
    print()
    print(f"{SPACES * ' '}count {{master_password}}")
    print(f"{SPACES * 2 * ' '}count the number of records")
    print()
    print(f"{SPACES * ' '}list {{master_password}}")
    print(f"{SPACES * 2 * ' '}list all the records")
    print()

def init():
    write(master_password=argv[2], data=b"Password manager")
    print("Password manager initialized.")

def check():
    master_password = argv[2]

    try:
        f = open('vault', 'rb')
    except FileNotFoundError:
        print("Vault file not found. Please use the init command to create a new vault.")
        exit(1)
    d = f.read()
    salt = d[:SALT_UPPER_BOUND]
    nonce = d[SALT_UPPER_BOUND:NONCE_UPPER_BOUND]
    tag = d[NONCE_UPPER_BOUND:TAG_UPPER_BOUND]
    ciphertext = d[TAG_UPPER_BOUND:]

    try:
        key = scrypt(master_password, salt, 16, N=2**18, r=8, p=1)
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

    print(f'Stored password for {address}')
    
    
def get():
    password_dictionary = check()
    address = argv[3]

    try:
        password = password_dictionary[address]
        print(f'Password for {address} is: {password}')
    except KeyError:
        print(f'Password for {address} was never saved.')

def count():
    password_dictionary = check()
    print(f'There are {len(password_dictionary)} passwords saved.')

def list():
    password_dictionary = check()
    print("Saved passwords:")
    for key in password_dictionary:
        print(f"{SPACES * ' '}{key} - {password_dictionary[key]}")

if __name__ == "__main__":
    verify_args()
    if argv[1] == "help":
        help()
    elif argv[1] == "init":
        init()
    elif argv[1] == "put":
        put()
    elif argv[1] == "get":
        get()
    elif argv[1] == "count":
        count()
    elif argv[1] == "list":
        list()