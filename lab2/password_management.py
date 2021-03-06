from getpass import getpass
from base64 import b64encode
from Crypto.Protocol.KDF import bcrypt

# funkcija čita i obrađuje unos lozinke sa standardnog ulaza
def read_password():

    counter = 0

    while True:
        pass1 = getpass("Password:")
        if len(pass1) < 8:
            print("Password must be at least 8 characters long!")
            continue
        pass2 = getpass("Repeat password:")
        if pass1 == pass2:
            break
        print("Passwords mismatching!")
        counter += 1
        if counter == 3:
            print("Mismatching passwords submitted too many times!")
            exit(1)

    return pass1

# funkcija čita i obrađuje unos lozinke onda kada korisnik mijenja svoju lozinku
def new_password(old_salt, hash):
    
    counter = 0
    while True:
        pass1 = getpass("New password:")
        if len(pass1) < 8:
            print("Password must be at least 8 characters long!")
            continue
        pass2 = getpass("Repeat new password:")
        if pass1 == pass2:
            password = pass1.encode('utf-8')
            b64password = b64encode(password)
            bcrypt_hash = bcrypt(b64password, 14, old_salt)

            if hash == bcrypt_hash:
                print("New password can't be the same as old password!")
                continue

            else:
                break

        print("Passwords mismatching!")
        counter += 1
        if counter == 3:
            print("Mismatching passwords submitted too many times!")
            exit(1)

    return pass1

# funkcija računa kriptografski sažetak lozinke na temelju same lozinke, salta i funkcije bcrypt
def hash_password(password, salt):
    
    password = password.encode('utf-8')
    b64password = b64encode(password)
    bcrypt_hash = bcrypt(b64password, 14, salt)

    return bcrypt_hash