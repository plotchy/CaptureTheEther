import sys
from dotenv import dotenv_values
PROJECT_SCRIPTS_PATH = dotenv_values(".env")["CTF_PROJECT_PATH"] + "/scripts/"
PROJECT_BUILD_PATH = dotenv_values(".env")["CTF_PROJECT_PATH"] + "/build/"
sys.path.insert(1, PROJECT_SCRIPTS_PATH)
from helpful_scripts import get_account, padHexTo32Bytes
from brownie import network, config, Contract
import time
from web3 import Web3, HTTPProvider
import json


def main():
    with open(PROJECT_BUILD_PATH + "contracts/CaptureTheEther.json") as f:
        info_json = json.load(f)
    CTEabi = info_json["abi"]

    with open(PROJECT_BUILD_PATH + "contracts/NicknameChallenge.json") as f:
        info_json = json.load(f)
    checkerabi = info_json["abi"]


    CTE_Contract_Address = "0x71c46Ed333C35e4E6c62D32dc7C8F00D125b4fee"
    nicknameContract = Contract.from_abi(name="CaptureTheEther", address=CTE_Contract_Address,abi=CTEabi)
    checker_Contract_Address = "0x57AF10539058C68d77E11B542652C8c4a4163896"
    checkerContract = Contract.from_abi(name="NicknameChallenge", address=checker_Contract_Address,abi=checkerabi)

    account = get_account()
    myHexName = Web3.toHex(text='plotchy')[2:]
    myHexName = padHexTo32Bytes(myHexName, "lower")
    print(myHexName)
    # name_tx = nicknameContract.setNickname(myHexName, {"from": account})
    # name_tx.wait(1)
    isComplete = checkerContract.isComplete()
    print(isComplete)
    myName = nicknameContract.nicknameOf("0x2A1e0000010D393CF93F89000000617A00d50000")
    print(myName)


    print('Done')


if __name__ == "__main__":
    main()