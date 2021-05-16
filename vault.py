#! /usr/bin/env python3
import os
import json
from FileIO import FileIO
from Encryption.fernet import Encryptor
class Vault:
    """
        Main vault class that does all the vault activities when the user get successfully authenticated.
        Only one vault can be opened at a given time by a single instance of the PWM.
    """
    __instance = None
    __FileIO = FileIO.getInstance()
    __Encryptor = Encryptor.getInstance()
    @staticmethod
    def getInstance():
        """
            Since the class is static, you need a getinstance method.
        """
        if Vault.__instance == None:
            Vault()
        return Vault.__instance
    def __init__(self) -> None:
        if Vault.__instance != None:
            raise Exception("There can only be one Vault instance")
        else:
            Vault.__instance = self
    @staticmethod
    def print_vault_menu() -> None:
        """
            Prints the vault interactive menu
        """
        print(
            """ Vault Options
            1 - Acess Complete Vault
            2 - Add New Item
            3 - Update Existing Item
            4 - Delete Item
            5 - Exit Vault
            """
        )
    @staticmethod
    def access_vault(uname: str):
        while True:
            Vault.print_vault_menu()
            print("Choice: ", end = "")
            op = input()
            if op == "1":
                Vault.__open_vault(uname)
            elif op == "2":
                Vault.__add_item(uname)
            elif op == "3":
                Vault.__update_item(uname)
            elif op == "4":
                Vault.__delete_item(uname)
            elif op == "5":
                break
            else:
                print("Invalid Choice")
    @staticmethod
    def __print_vault_items(item: str, uname: str, password:str):
        print("Item: ", item)
        print("Username: ", uname)
        print("Password: ", Encryptor.decrypt_pass(password))
        print("")
        print("")
        print("")
    @staticmethod
    def __open_vault(uname: str):
        vault_dict = Vault.__FileIO.open_vault(uname)
        os.system("clear")
        if len(vault_dict) == 0:
            print ("The vault is currently empty")
            return
        print("-----------------------------"+ uname+"\'s vault---------------------------------")
        for key in vault_dict.keys():
            for subkeys in vault_dict[key].keys():
                Vault.__print_vault_items(key, subkeys, vault_dict[key][subkeys])
        print("press enter key to quit")
        input()
        os.system("clear")
    @staticmethod
    def __add_item(uname: str):
        vault_dict = Vault.__FileIO.open_vault(uname)
        print ("Enter the name of the item: ", end="")
        item = input()
        itemurl = "https://www."+item.lower()+".com"
        print("Please enter the username for this item: ", end="")
        username = input()
        if itemurl in vault_dict and username in vault_dict[itemurl]:
            print("Error, username already exists, to update existing item, choose the update option from the menu")
            return
        print("Please enter the password for this item: ", end="")
        password = input()
        new_item_dict = {username:Vault.__Encryptor.encrypt_pass(password)}
        if itemurl in vault_dict:
            vault_dict[itemurl].update(new_item_dict)
        else:
            vault_dict.update({itemurl: new_item_dict})
        Vault.__FileIO.update_vault(uname, vault_dict)
    @staticmethod
    def __update_item(uname: str):
        vault_dict = Vault.__FileIO.open_vault(uname)
        print ("Enter the name of the item you would like to update: ", end="")
        item = input()
        itemurl = "https://www."+item.lower()+".com"
        if itemurl not in vault_dict:
            print(" Item \'"+item+"\' doesnt exist in the vault")
            return
        print ("All items for \'"+item+"\', which one would you like to update?")
        for usernames in vault_dict[itemurl].keys():
            print(usernames)
        print ("Username: ", end="")
        username = input()
        if username not in vault_dict[itemurl]:
            print("Incorrect or non-existent username entered!")
            return
        print ("Please enter the new password: ", end="")
        newpass = input()
        vault_dict[itemurl][username] = Vault.__Encryptor.encrypt_pass(newpass)
        Vault.__FileIO.update_vault(uname, vault_dict)
        
    @staticmethod
    def __delete_item(uname: str):
        vault_dict = Vault.__FileIO.open_vault(uname)
        print ("Enter the name of the item you would like to delete: ", end="")
        item = input()
        itemurl = "https://www."+item.lower()+".com"
        if itemurl not in vault_dict:
            print(" Item \'"+item+"\' doesnt exist in the vault")
            return
        print ("All items for \'"+item+"\', which one would you like to delete?")
        for usernames in vault_dict[itemurl].keys():
            print(usernames)
        print ("Username: ", end="")
        username = input()
        if username not in vault_dict[itemurl]:
            print("Incorrect or non-existent username entered!")
            return
        del vault_dict[itemurl][username]
        if len(vault_dict[itemurl]) == 0:
            del vault_dict[itemurl]
        Vault.__FileIO.update_vault(uname, vault_dict)

