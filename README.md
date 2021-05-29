# Simple Password Manager

A simple password manager created for security and pen-testing purposes for our project for the class for CS-205 at University of California, Irvine taught by Dr Qi Alfred Chen.

Co-Contributers are **Andre Roesti** and **Neeraj Dharmadhikari**

## Dependencies
```
cryptography
json
getpass
pyotp
```
- All of these can be installed via pip
- Additionally, create `Store` directory in the main directory as well as create `Store/users.txt` beforehand.

## Vault Manager Usage

- You can run the password manager by calling `python3 main.py`. This will run the main password manager. 
- The user database and each user vault is stored in `Store` directory and encryption keys are stored in `Secret` directory.

## Two Factor Authenticator Usage

- To enable 2FA for your vault, authenticate with your username and password. Selecting option 4 will allow you to set up new 2FA. The secret key will be printed in plain text which you will require to generate OTPs via `TwoFApp.py` module. Additionally, you can also delete existing 2FA if you wish to.

- If Two Factor Authentication is enabled for your vault, please record and save the **Secret OTP Key**.
- To generate OTP, run the `TwoFApp.py` module separately by calling `python3 TwoFApp.py <Secret OTP Key>`. The OTPs generated are time based and are refreshed every 30 seconds.

### Options
List of Main Menu options:
```
1. Add user
2. Delete user
3. Access Vault
4. Modify Two Factor Authentication
5. Quit
```

List of 2FA options:
```
1 - Add New 2FA
2 - Delete Existing 2FA
```

List of Vault Menu options:
```
1 - Acess Complete Vault
2 - Add New Item
3 - Update Existing Item
4 - Delete Item
5 - Exit Vault
```
## Future Work

As more features are implemented, this README file will be updated.
