#! /usr/bin/env python3

import getpass
from json.decoder import JSONDecodeError
import os
import json
from cryptography.fernet import Fernet
from UI import UserInterface
DEBUG = True

PASSWORD_RETRIES = 3

CRED_KEY = b'uzGeNH-N7a8yjVjNTGcJE5PSJnWdqOxRQ3XU9Fh2CbE='

cfile = "Store/users.txt"
cred_encryptor = Fernet(CRED_KEY)

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
            #show_pass(data[uname])
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

def authenticate_user(uname: str) -> bool:
    """
        Authenticates the user for deleting user or managing their vault
    """
    data = {}
    cred_file = open(cfile, "r")
    try:
        data = json.load(cred_file)
        if uname not in data:
            print("User " + uname + " does not exist!")
            cred_file.close()
            return
        """
            Check here for cooldown
        """
        cred_file.close()
        hashed_pass = decrypt_credentials(data[uname])
        retries = PASSWORD_RETRIES
        while retries > 0:
            password = getpass.getpass("Password: ")
            if password != hashed_pass:
                print("Error!, Incorrect Password entered!")
                retries-=1
                print("Retries left: ", retries)
            else:
                return True
    except JSONDecodeError:
        print("No users are created")
        return
    
    print("No password retries left!")

    """
        Time out user here
    """
    return False

def delete_user() -> None:
    """
        Deletes a user and removes their vault
    """
    print("Enter the username: ", end ="")
    uname = input()
    if authenticate_user(uname) == True:
        vault_path = "Store/"+uname+".vault"
        cred_file = open(cfile, "r")
        data = json.load(cred_file)
        cred_file.close()
        cred_file = open(cfile, "w")
        del data[uname]
        os.remove(vault_path)
        json.dump(data, cred_file, indent=4)
        cred_file.close()
        return
    

def access_vault() -> None:
    """
        Opens the vault for the user and they can access their passwords for their saved sites.
    """
    print("Enter the username: ", end ="")
    uname = input()
    if authenticate_user(uname) == True:
        print("Authentication Successful!") # Placeholder for now
    

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
    return

    
if __name__ == "__main__":
    main()
