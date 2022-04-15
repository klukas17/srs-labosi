#!/usr/bin/env python3

from sys import argv
from vault_management import read_vault, write_vault
from password_management import hash_password, new_password
from getpass import getpass
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes

# funkcija koja provjerava ispravnog unešenih argumenata
def verify_args():
    if len(argv) <= 1:
        print("Missing arguments! First argument must be {username}.")
        exit(1)
    elif len(argv) > 2:
        print("Wrong arguments! Arguments must be in '{username}' format.")
        exit(1)

# funkcija koja se poziva u slučaju neuspjelog pokušaja prijave
def fail():
    print("Username or password incorrect.")
    exit(1)

# funkcija koja vrši login
def login():
    vault = read_vault()
    usr = argv[1]

    password = getpass("Password:")

    # potrebno radno čekanje kako bi jednako trajala neuspjela prijava zbog nepostojećeg korisničkog imena i krive lozinke
    if usr not in vault:
        pswd = hash_password("random", get_random_bytes(16))
        fail()

    hash = b64decode(vault[usr][0][1:])
    salt = b64decode(vault[usr][1][1:])
    change = vault[usr][2]

    pswd = hash_password(password, salt)

    if pswd != hash:
        fail()

    if change == "1":

        old_salt = salt
        salt = get_random_bytes(16)
        hash = hash_password(new_password(old_salt, hash), salt)
        vault[usr] = (b64encode(hash), b64encode(salt), 0)
        write_vault(vault)

    print("Login successful.")

if __name__ == "__main__":
    verify_args()
    login()