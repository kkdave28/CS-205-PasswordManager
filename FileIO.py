from json.decoder import JSONDecodeError
import json
import os
CFILE = "Store/users.txt"

class FileIO:
    __instance = None
    __current_vault = None
    @staticmethod
    def getInstance():
        """
            Since the class is static, you need a getinstance method.
        """
        if FileIO.__instance == None:
            FileIO()
        return FileIO.__instance
    def __init__(self) -> None:
        if FileIO.__instance != None:
            raise Exception("There can only be one instance of FileIO")
        else:
            FileIO.__instance = self
    @staticmethod
    def load_cred() -> dict:
        """
            Loads the credentials from the users database
        """
        cred_file = open(CFILE, "r")
        data = {}
        try:
            data = json.load(cred_file)
        except JSONDecodeError:
            pass
        cred_file.close()
        return data
    @staticmethod 
    def update_cred(new_data: dict):
        """
            Updates the credentials and pushes it to the users database
        """
        cred_file = open(CFILE, "w")
        json.dump(new_data, cred_file, indent=4)
        cred_file.close()
    @staticmethod 
    def create_vault(uname: str):
        """
            Create a vault for a new user
        """
        new_vault = "Store/"+uname+".vault"
        vault = open(new_vault, "w")
        vault.close()
    @staticmethod
    def delete_vault(uname: str):
        """
            Delete the vault when the user delete's their account
        """
        vault_path = "Store/"+uname+".vault"
        os.remove(vault_path)
    @staticmethod
    def open_vault(uname: str)-> dict:
        """
            OPens the vault, get the data into a dictionary and return the data
        """
        vault_path = "Store/"+uname+".vault"
        data = {}
        vfile = None
        try:
            vfile = open(vault_path, "r")
            data = json.load(vfile)
            vfile.close()
            return data
        except FileNotFoundError:
            print("User "+uname+" does not exist. Vault does not exist.")
            return data
        except JSONDecodeError:
            vfile.close()
            return data
    @staticmethod 
    def update_vault(uname: str, new_dict: dict):
        """
            Push the updates to the user vault
        """
        vault_path = "Store/"+uname+".vault"
        try:
            vfile = open(vault_path, "w")
            json.dump(new_dict, vfile, indent=4)
            vfile.close()
        except FileNotFoundError:
            print("uhh, how did we get here?, fileio.update_vault")
