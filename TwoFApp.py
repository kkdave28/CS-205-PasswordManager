import pyotp
import sys

def generate_otp(key: str):
    totp = pyotp.TOTP(key)
    option = ""
    while(option != "q"):
        print("Your OTP is: ", totp.now())
        print("")
        print("Enter q to quit, press enter to generate OTP.")
        option = input()
        

if __name__ == "__main__":
    generate_otp(sys.argv[1])
