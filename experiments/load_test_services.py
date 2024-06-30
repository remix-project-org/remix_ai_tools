
# In locust.py
from locust import HttpUser, task, constant, between
import random, requests
import json

##############################################################################################################################
##############################################################################################################################
#################################### Important Note: There is a rate limiter #################################################
####################################      on the public url server side      #################################################
##############################################################################################################################
##############################################################################################################################

url = "https://solcoder.remixproject.org"
no_rate_limit_url = "https://xofsxrwr8zkja6-7861.proxy.runpod.net/ai/api/"

file_content ="""
pragma solidity >=0.8.2 <0.9.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
 */
contract Storage {

    uint256 number;

    /**
     * @dev Store value in variable
     * @param num value to store
     */
    function store(uint256 num) public {
        number = num;
    }

    /**
     * @dev Return value 
     * @return value of 'number'
     */
    function retrieve() public view returns (uint256){
        return number;
    }
}""" 
        
class QuickstartUser(HttpUser):
    wait_time = between(min_wait=10, max_wait=60)
    host = "https://solcoder.remixproject.org"

#     @task
#     def test_code_generation(self):
#         self.client.post(no_rate_limit_url + "code_completion", 
#         json={  "data":[# convert dictionary to string
#             """// SPDX-License-Identifier: GPL-3.0

# pragma solidity >=0.7.0 <0.9.0;

# /** 
#  * @title Ballot
#  * @dev Implements voting process along with vote delegation
#  */
# contract Ballot {

#     struct Voter {
#         uint weight; // weight is accumulated by delegation
#         bool voted;  // if true, that person already voted
#         address delegate; // person delegated to
#         uint vote;   // index of the voted proposal
#     }

#     struct Proposal {
#         // If you can limit the length to a certain number of bytes, 
#         // always use one of bytes1 to bytes32 because they are much cheaper
#         bytes32 name;   // short name (up to 32 bytes)
#         uint voteCount; // number of accumulated votes
#     }

#     address public chairperson;

#     mapping(address => Voter) public voters;

#     Proposal[] public proposals;

#     /** 
#      * @dev Give 'voter' the right to vote on this ballot. May only be called by 'chairperson'.
#      * @param voter address of voter
#      */
#     function giveRightToVote(address voter) public {
#         require(
#             msg.sender == chairperson,
#             "Only chairperson can give right to vote."
#         );
#         require(
#             !voters[voter].voted,
#             "The voter already voted."
#         );
#         require(voters[voter].weight == 0);
#         voters[voter].weight = 1;
#     }
#     /// Function for casting a user vote using the struct Vote",
# """
#             "",
#             "",
#             False,
#             1000,
#             0.9,
#             0.92,
#             50
#         ]})

    # @task
    # def test_code_explaining(self):
    #     self.client.post(no_rate_limit_url + "code_explaining", 
    #     json={  "data":[# convert dictionary to string
    #         file_content,
    #         False,
    #         2000,
    #         0.9,
    #         0.92,
    #         50,
    #         ""
    #     ]})

    # @task
    # def test_code_explaining_with_context(self):
    #     self.client.post(no_rate_limit_url + "code_explaining", 
    #     json={  "data":[
    #         """function retrieve() public view returns (uint256){
    #     return number;
    # }""",
    #         False, 2000, 0.9, 0.92, 50, file_content
    #     ]})



#     @task
#     def test_error_explaining(self):
#         errorText = """TypeError: Data location must be "storage", "memory" or "calldata" for variable, but none was given.
#   --> contracts/3_Ballot.sol:84:9:
#    |
# 84 |         Voter delegate_ = voters[to];
#    |         ^^^^^^^^^^^^^^^
# """
#         self.client.post(no_rate_limit_url + "error_explaining", 
#         json={  "data":[
#             f"solidity code: {file_content}\n error message: {errorText}\n explain why the error occurred and how to fix it.",
#             False,2000,0.9,0.8,50
#         ]})

# #     @task
# #     def test_contract_generation(self):
# #         self.client.post(no_rate_limit_url + "contract_generation", 
# #         json={  "data":[
# #             "generate a simple storage contract with events and functions",
# #             False,2000,0.9,0.8,50

# #         ]}) 

    @task
    def test_answering(self):
        self.client.post(no_rate_limit_url + "solidity_answer", 
        json={  "data":[
            "sol-gpt What is the purpose of the following code snippet? \n```solidity\nfunction store(uint256 num) public {\n    number = num;\n}\n```",
            False,1000,0.9,0.8,50
        ]})