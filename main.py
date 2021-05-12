#! /usr/bin/env python3

import getpass
from json.decoder import JSONDecodeError
import os
import json
from cryptography.fernet import Fernet
DEBUG = True
CRED_KEY = b'uzGeNH-N7a8yjVjNTGcJE5PSJnWdqOxRQ3XU9Fh2CbE='
DBASE_KEY = b'0-DwIS53LQ4H_IY8MI5VSQ-qI1Lf4TSGiXCmGiNjFRQ='
cfile = "Store/users.txt"
cred_encryptor = Fernet(CRED_KEY)
dbase_encryptor = Fernet(DBASE_KEY)

def dbug(msg: str)-> None:
    """
        Debug print function to test functionality and find potential bugs
    """
    if DEBUG:
        print(msg)

def encrypt_credentials(value: str)-> str:
    """
        Encrypts password string that is used to access the vault
    """
    protected_str = cred_encryptor.encrypt(str.encode(value))
    return protected_str.decode()

def decrypt_credentials(value: str) -> str:
    """
        Encrypts password string that is used to access the vault
    """
    decrypted_str = cred_encryptor.decrypt(str.encode(value))
    return decrypted_str.decode()

def show_pass(value: str) -> None:
    """
        Debug function
    """
    print(decrypt_credentials(value))

def add_user() -> None:
    """
       adds a user and creates a vault 
    """
    print("Please enter a username: ", end = "")
    uname = input()
    password = getpass.getpass("Please enter a strong password: ")
    encrypted_cred = encrypt_credentials(password)
    cred_file = open(cfile, "r")
    data = {}
    try:
        data = json.load(cred_file)
        if uname in data:
            print("User " + uname + " already exists!")
            show_pass(data[uname])
            cred_file.close()
            return
    except JSONDecodeError:
        pass
    cred_file.close()
    new_creds = {uname : encrypted_cred}
    data.update(new_creds)
    cred_file = open(cfile, "w")
    json.dump(data, cred_file, indent=4)
    cred_file.close()
    new_vault = "Store/"+uname+".vault"
    vault = open(new_vault, 'w')
    vault.close()
    return


def delete_user() -> None:
    """
        Deletes a user and removes their vault
    """
    uname = ""
    data = {}
    cred_file = open(cfile, "r")
    try:
        data = json.load(cred_file)
        print("Please enter the username: ", end = "")
        uname = input()
        if uname not in data:
            print("User " + uname + " does not exist!")
            cred_file.close()
            return
        cred_file.close()
        hashed_pass = decrypt_credentials(data[uname])
        retries = 3
        while retries > 0:
            password = getpass.getpass("Password: ")
            if password != hashed_pass:
                print("Error!, Incorrect Password entered!")
                retries-=1
                print("Retries left: ", retries)
            else:
                del data[uname]
                vault_path = "Store/"+uname+".vault"
                cred_file = open(cfile, "w")
                os.remove(vault_path)
                json.dump(data, cred_file, indent=4)
                cred_file.close()
                return
    except JSONDecodeError:
        print("No users are created")

def access_vault() -> None:
    pass

def main() -> None:
    """
        Main process that runs the password manager
    """
    print("------------------------------Password Manager Test Suite--------------------------------------------")
    while True:
        print(""" Options
        1 - Add user
        2 - Delete user
        3 - Access Vault
        4 - Quit
        """)
        op = input()
        if op == "1":
            add_user()
        elif op == "2":
            delete_user()
        elif op == "3":
            access_vault()
        elif op == "4":
            break

    """
    print("Username: ", end = "")
    user = input()
    password = getpass.getpass("Password: ")
    dbug("Username Entered: "+user)
    dbug("Password Entered: "+password)
    encrypted_cred = encrypt_credentials((user, password))
    dbug("Encrypted user = " + encrypted_cred[0])
    dbug("Encrypted pass = " + encrypted_cred[1])
    decrypted_cred = decrypt_credentials((encrypted_cred[0], encrypted_cred[1]))
    dbug("Decrypted user = " + decrypted_cred[0])
    dbug("Decrypted pass = " + decrypted_cred[1])
    """
    return

    
if __name__ == "__main__":
    main()
