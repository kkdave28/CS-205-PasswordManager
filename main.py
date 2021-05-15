#! /usr/bin/env python3
from cryptography.fernet import Fernet
from UI import UserInterface
DEBUG = True
MainUI = UserInterface.getInstance()
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
            MainUI.add_user()
        elif op == "2":
            MainUI.delete_user()
        elif op == "3":
            MainUI.access_vault()
        elif op == "4":
            break
    return 0

    
if __name__ == "__main__":
    main()
