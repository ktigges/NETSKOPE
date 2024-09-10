

# Author.....: Kevin Tigges
# Script Name: common.py
# Desc.......: Common Functions used by many programs
# 
#
# Last Updates: 9/9/2024
# v001
#

from cryptography.fernet import Fernet
import os

def get_api():
# Password/API Key is encrypted so it is not present in this script and is read from 2 files containing the encrypted password and key
# There is a script called encryptpwd.py that should be used to generate the encrypted password to be used prior to using this script
#
# Place the password in a file called pwd.txt (This will be deleted once the encrypted password is generated)
# Run the script - python3 ./encryptpwd.py
# 2 files will be generated that should be kept in the script directory and will be utilized to authenticate below
#
# read encrypted pwd and convert into byte
#
    cwd = './'
    with open('./apipass.txt') as f:
        apipwd = ''.join(f.readlines())
        encpwdbyt = bytes(apipwd, 'utf-8')
    f.close()

    # read key and convert into byte
    with open('./apikey.txt') as f:
        refKey = ''.join(f.readlines())
        refKeybyt = bytes(refKey, 'utf-8')
    f.close()

    # use the key and decrypt the password

    keytouse = Fernet(refKeybyt)
    # Convert the password from byte to Ascii
    api_key = (keytouse.decrypt(encpwdbyt)).decode('ASCII')
    return api_key.strip()


