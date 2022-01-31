import sys
from dotenv import dotenv_values
PROJECT_SCRIPTS_PATH = dotenv_values(".env")["CTF_PROJECT_PATH"] + "/scripts/"
PROJECT_BUILD_PATH = dotenv_values(".env")["CTF_PROJECT_PATH"] + "/build/"
sys.path.insert(1, PROJECT_SCRIPTS_PATH)
from helpful_scripts import get_account, padHexTo32Bytes
from brownie import Contract
from web3 import Web3
import json
PUBLIC_KEY = dotenv_values(".env")["PUBLIC_KEY"]


def main():
    ###########
    # SETUP
    ###########
    with open(PROJECT_BUILD_PATH + "contracts/GuessTheNumberChallenge.json") as f:
        info_json = json.load(f)
    Challenge_ABI = info_json["abi"]
    Challenge_Address = "0x8410069eb3972d75aeb993201Cc9D5A7Dcc8911d"
    challengeContract = Contract.from_abi(name="", address=Challenge_Address,abi=Challenge_ABI)
    account = get_account()

    ###########
    # SOLVING
    ###########
    guess_tx = challengeContract.guess(42, {"from": account, "value": Web3.toWei(1, unit="ether")})


    ###########
    # CHECKING
    ###########
    guess_tx.wait(1)
    isComplete = challengeContract.isComplete()
    print(isComplete)



    print('Finished')


if __name__ == "__main__":
    main()