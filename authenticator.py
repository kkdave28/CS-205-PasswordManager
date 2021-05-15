import getpass
from json.decoder import JSONDecodeError
import json
from Encryption.fernet import Encryptor
from FileIO import FileIO
from datetime import datetime, timezone, timedelta
DEBUG = True
PASSWORD_RETRIES = 3
TIMEOUT = 120

cfile = "Store/users.txt"

class Authenticator:
    __instance = None
    __Encrypter = Encryptor.getInstance()
    __FileIO = FileIO.getInstance()
    __cooldown = {}
    @staticmethod
    def getInstance():
        """
            Since the class is static, you need a getinstance method.
        """
        if Authenticator.__instance == None:
            Authenticator()
        return Authenticator.__instance
    def __init__(self) -> None:
        if Authenticator.__instance != None:
            raise Exception("There can be only one instance of Authenticator")
        else:
            Authenticator.__instance = self
            
    @staticmethod
    def authenticate_user(uname: str) -> bool:
        """
            Authenticates the user for deleting user or managing their vault
        """
        data = Authenticator.__FileIO.load_cred()
        if uname not in data:
            print("User " + uname + " does not exist!")
            return
        if uname in Authenticator.__cooldown and Authenticator.__cooldown[uname] > datetime.now(timezone.utc):
            print("Error! Trying to access the vault too many times in a short time")
            cooldown_period = Authenticator.__cooldown[uname] - datetime.now(timezone.utc)
            print("Please try again after ", cooldown_period.total_seconds(), " seconds.")
            return False
        hashed_pass = Authenticator.__Encrypter.decrypt_cred(data[uname])
        #hashed_pass = decrypt_credentials(data[uname])
        retries = PASSWORD_RETRIES
        while retries > 0:
            password = getpass.getpass("Password: ")
            if password != hashed_pass:
                print("Error!, Incorrect Password entered!")
                retries-=1
                print("Retries left: ", retries)
            else:
                return True
        
        print("No password retries left!")
        Authenticator.__cooldown[uname] = datetime.now(timezone.utc) + timedelta(0, 120)
        """
            Time out user here
        """
        return False