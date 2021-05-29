from cryptography.fernet import Fernet
PATH_TO_KEYS = "/home/kkdave/CS-205-Project/PasswordManager/Secret/keys.txt"
keys = []
with open(PATH_TO_KEYS, "r") as key_file:
    keys = key_file.read().splitlines()
class Encryptor:
    __instance = None
    __dbase_key = str.encode(keys[0])
    __cred_key = str.encode(keys[1])
    __cred_encryptor = Fernet(__cred_key)
    __dbase_encryptor = Fernet(__dbase_key)
    @staticmethod
    def getInstance():
        """
            Since the class is static, you need a getinstance method.
        """
        if Encryptor.__instance == None:
            Encryptor()
        return Encryptor.__instance
    def __init__(self) -> None:
        if Encryptor.__instance != None:
            raise Exception("There can only be one Fernet Encryptor instance")
        else:
            Encryptor.__instance = self
    @staticmethod
    def encrypt_cred(value: str) -> str:
        """
            Encrypts the user credentials
        """
        protected_str = Encryptor.__cred_encryptor.encrypt(str.encode(value))
        return protected_str.decode()
    @staticmethod
    def decrypt_cred(value: str) -> str:
        """
            Decrypts the user credentials
        """
        decrypted_str = Encryptor.__cred_encryptor.decrypt(str.encode(value))
        return decrypted_str.decode()
    @staticmethod
    def encrypt_pass(value: str) -> str:
        """
            Encrypts a user vault password.
        """
        protected_str = Encryptor.__dbase_encryptor.encrypt(str.encode(value))
        return protected_str.decode()
    @staticmethod
    def decrypt_pass(value: str) -> str:
        """ 
            Decrypts the user vault password
        """
        decrypted_str = Encryptor.__dbase_encryptor.decrypt(str.encode(value))
        return decrypted_str.decode()