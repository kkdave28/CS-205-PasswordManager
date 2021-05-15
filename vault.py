#! /usr/bin/env python3

import getpass
from json.decoder import JSONDecodeError
import os
import json
from cryptography.fernet import Fernet

DBASE_KEY = b'0-DwIS53LQ4H_IY8MI5VSQ-qI1Lf4TSGiXCmGiNjFRQ='
dbase_encryptor = Fernet(DBASE_KEY)


class Vault:
    """
        Main vault class that does all the vault activities when the user get successfully authenticated
    """
    __instance = None
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
