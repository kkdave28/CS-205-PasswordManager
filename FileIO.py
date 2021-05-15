from json.decoder import JSONDecodeError
import json
import os
CFILE = "Store/users.txt"

class FileIO:
    __instance = None
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
        cred_file = open(CFILE, "w")
        json.dump(new_data, cred_file, indent=4)
        cred_file.close()
    @staticmethod 
    def create_vault(uname: str):
        new_vault = "Store/"+uname+".vault"
        vault = open(new_vault, "w")
        vault.close()
    @staticmethod
    def delete_vault(uname: str):
        vault_path = "Store/"+uname+".vault"
        os.remove(vault_path)
