# Capture The Ether

This is a Capture the flag (CTF) challenge hosted at [CaptureTheEther](https://www.capturetheether.com). This repo contains my solutions to the challenges written with Python, Brownie, and Solidity.

## Note On Security

For private key security, several setup files are not uploaded to this repo and have been included in the .gitignore file.
Several import statements reference packages I've written for decrypting my keys, and scripts/helpful_scripts.py especially references these functions.

## General Learnings

*Predict The Future*
Cannot rely on `while(not challengeContract.isComplete()):` to end code execution. Unsure if the RPC is unreliable, but further iterations of the loop were executed after the challenge was completed and a block confirmation happened beforehand. There might be separate brownie api that resolves this better - such as `challengeContract.isComplete().result`

Gas simulation and estimation does not perform well for contracts that perform separate actions based on randomness. I felt pain when the 1/10 chance succeeded but my call ran out of gas.

