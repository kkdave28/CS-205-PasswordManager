import getpass
from json.decoder import JSONDecodeError
from vault import Vault
from FileIO import FileIO
import os
import json
from Encryption.fernet import Encryptor
from authenticator import Authenticator


class UserInterface:
    __instance = None
    __Encryptor = Encryptor.getInstance()
    __FileIO = FileIO.getInstance()
    __Authenticator = Authenticator.getInstance()
    __Vault = Vault.getInstance()
    @staticmethod
    def getInstance():
        """
            Since the class is static, you need a getinstance method.
        """
        if UserInterface.__instance == None:
            UserInterface()
        return UserInterface.__instance
    def __init__(self) -> None:
        if UserInterface.__instance != None:
            raise Exception("There can only be one UI interface")
        else:
            UserInterface.__instance = self
    @staticmethod
    def add_user() -> None:
        """
            Method to add a user to the user database and create a vault for the new user.
        """
        data = UserInterface.__FileIO.load_cred()
        print("Please enter a username: ", end = "")
        uname = input()
        if uname in data:
            print("User \"" + uname + "\" already exists!")
            return
        password = getpass.getpass("Please enter a strong password: ")
        encrypt_credentials = UserInterface.__Encryptor.encrypt_cred(password)
        new_cred = {uname:encrypt_credentials}
        data.update(new_cred)
        UserInterface.__FileIO.update_cred(data)
        UserInterface.__FileIO.create_vault(uname)
    
    @staticmethod
    def delete_user():
        """
            Method to delete a user from the databse and remove their vault.
        """
        print("Enter the username: ", end ="")
        uname = input()
        if UserInterface.__Authenticator.authenticate_user(uname):
            data = UserInterface.__FileIO.load_cred()
            del data[uname]
            UserInterface.__FileIO.update_cred(data)
            UserInterface.__FileIO.delete_vault(uname)
    @staticmethod
    def access_vault():
        """
            Method to allow the user to access their vault.
        """
        print("Enter the username: ", end ="")
        uname = input()
        if UserInterface.__Authenticator.authenticate_user(uname):
            print("Welcome to your vault!")
            UserInterface.__Vault.access_vault(uname)
            
    @staticmethod
    def clear_screen():
        """
            Method to clear screen for better visibility.
        """
        os.system("clear")
    @staticmethod
    def print_main_menu() -> None:
        """
            Prints the main interactive menu
        """
        print("""           Options
        1 - Add user
        2 - Delete user
        3 - Access Vault
        4 - Quit
        """)
    