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

# Run using: brownie run scripts/challenges/GuessTheSecretNumber/guesssecret.py --network ropsten

def main():
    ###########
    # SETUP
    ###########
    with open(PROJECT_BUILD_PATH + "contracts/GuessTheSecretNumberChallenge.json") as f:
        info_json = json.load(f)
    Challenge_ABI = info_json["abi"]
    Challenge_Address = "0x06240545E1c3D672662e87F54AF2761a29aBddF2"
    challengeContract = Contract.from_abi(name="", address=Challenge_Address,abi=Challenge_ABI)
    account = get_account()

    ###########
    # SOLVING
    ###########
    answerHash = "0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365"
    for guess in range(0, 256):
        guessHash = Web3.toHex(Web3.keccak(hexstr=Web3.toHex(guess)))
        print (guess, guessHash, answerHash)
        if guessHash == answerHash:
            break
    
    guess_tx = challengeContract.guess(guess, {"from": account, "value": Web3.toWei(1, 'ether')})

    ###########
    # CHECKING
    ###########
    guess_tx.wait(1)
    isComplete = challengeContract.isComplete()
    print(isComplete)

    print('Finished')

if __name__ == "__main__":
    main()