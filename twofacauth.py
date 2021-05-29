import pyotp

class TwoFa:
    __instance = None
    @staticmethod
    def getInstance():
        if TwoFa.__instance == None:
            TwoFa()
        return TwoFa.__instance
    
    def __init__(self) -> None:
        if TwoFa.__instance != None:
            raise Exception("There can only be one instance of TwoFa Authenticator")
        else:
            TwoFa.__instance = self

    @staticmethod
    def New2FA() -> str:
        key = pyotp.random_base32()
        print("Please enter this key into your 2FA python APP and do not share it with anyone!  ", key)
        return key
    
    @staticmethod
    def validate_otp(key: str, value: str) -> str:
        totp = pyotp.TOTP(key)
        return totp.verify(value)