#!/usr/bin/env python3

from sys import argv
from Crypto.Random import get_random_bytes
from base64 import b64encode
from vault_management import read_vault, write_vault
from password_management import hash_password, read_password

def verify_args():
    if len(argv) <= 1:
        print("Missing arguments! First argument can be add, passwd, forcepass, del, init.")
        exit(1)
    elif argv[1] == "add":
        if len(argv) != 3:
            print("Wrong arguments! Arguments for the add command must be in 'add {username}' format.")
            exit(1)
    elif argv[1] == "passwd":
        if len(argv) != 3:
            print("Wrong arguments! Arguments for the passwd command must be in 'passwd {username}' format.")
            exit(1)
    elif argv[1] == "forcepass":
        if len(argv) != 3:
            print("Wrong arguments! Arguments for the forcepass command must be in 'forcepass {username}' format.")
            exit(1)
    elif argv[1] == "del":
        if len(argv) != 3:
            print("Wrong arguments! Arguments for the del command must be in 'del {username}' format.")
            exit(1)
    elif argv[1] == "init":
        if len(argv) != 2:
            print("Wrong arguments! Arguments for the init command must be in 'init' format.")
    else:
        print("Wrong arguments! First argument can be add passwd, forcepass, del.")
        exit(1)

def new_password(vault, usr):

    salt = get_random_bytes(16)
    hash = hash_password(read_password(), salt)
    vault[usr] = (b64encode(hash), b64encode(salt), 0)

    return vault

def add():
    vault = read_vault()
    usr = argv[2]

    if usr in vault:
        print("Can't add user since they are already present.")
        exit(1)

    vault = new_password(vault, usr)
    
    write_vault(vault)

    print("User added successfully!")

def passwd():
    vault = read_vault()
    usr = argv[2]

    if usr not in vault:
        print("Can't change user's password as they are not present.")
        exit(1)

    vault = new_password(vault, usr)
    
    write_vault(vault)

    print("Password changed successfully!")

def forcepass():
    vault = read_vault()
    usr = argv[2]

    if usr not in vault:
        print("Can't force user to change their password as they are not present.")
        exit(1)

    vault[usr] = (vault[usr][0], vault[usr][1], 1)
    write_vault(vault)

    print("User will be required to change password on next login!")

def delete():
    vault = read_vault()

    usr = argv[2]

    if usr not in vault:
        print("Can't delete user as they are not present.")
        exit(1)

    vault.pop(usr)
    write_vault(vault)

    print("User deleted successfully!")

if __name__ == "__main__":
    verify_args()
    if argv[1] == "add":
        add()
    elif argv[1] == "passwd":
        passwd()
    elif argv[1] == "forcepass":
        forcepass()
    elif argv[1] == "del":
        delete()