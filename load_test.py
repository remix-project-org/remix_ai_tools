
# In locust.py
from locust import HttpUser, task, constant, between
import random, requests
import json

url = "https://hkfll35zthu6e2-7861.proxy.runpod.net/ai/api/"
class QuickstartUser(HttpUser):
    wait_time = between(min_wait=20, max_wait=30)
    host = ""

    # @task
    # def test_code_completion(self):
    #     self.client.post( url+"code_completion", 
    #     json={"data":[
    #         "// SPDX-License-Identifier: GPL-3.0\n pragma solidity >=0.8.2 <0.9.0;\n\n\ncontract Storage {\n\n    uint256 number; \n\n    ///write a function for adding 2 uint256 numbers and return the result",
    #         "", False, 200, 0.1, 0.9, 50
    #     ]})

    # @task
    # def test_code_generation(self):
    #     self.client.post( url + "code_generation", 
    #     json={"data":[
    #         "// SPDX-License-Identifier: GPL-3.0\n pragma solidity >=0.8.2 <0.9.0;\n\n\ncontract Storage {\n\n    uint256 number; \n\n    ///write a function for adding 2 uint256 numbers and return the result",
    #         False, 200, 0.1, 0.9, 50
    #     ]})


    @task
    def test_code_explaining(self):
        self.client.post( url + "code_explaining", 
        json={"data":[
            "// SPDX-License-Identifier: GPL-3.0\n pragma solidity >=0.8.2 <0.9.0;\n\n\ncontract Storage {\n\n    uint256 number; \n\n    ///write a function for adding 2 uint256 numbers and return the result",
            False, 200, 0.1, 0.9, 50
        ]})


    # @task
    # def test_error_explaining(self):
    #     self.client.post( url + "error_explaining", 
    #     json={"data":[
    #         "ParserError: Expected pragma, import directive or contract/interface/library/struct/enum/constant/function/error definition.--> contracts/1_Storage.sol:42:5:",
    #         False, 200, 0.1, 0.9, 50
    #     ]})


    # @task
    # def test_contract_generation(self):
    #     self.client.post( url + "contract_generation", 
    #     json={"data":[
    #         "Write a contract for a simple storage",
    #         False, 2000, 0.1, 0.9, 50
    #     ]})

    @task
    def test_answering(self):
        self.client.post( url + "solidity_answer", 
        json={"data":[
            "What is the purpose of the storage contract?",
            False, 2000, 0.1, 0.9, 50
        ]})

        
x = requests.post(url + "solidity_answer", 
        json={"data":[
            "What is the purpose of the storage contract?",
            False, 2000, 0.1, 0.9, 50
        ]},
        headers={"Content-Type": "application/json"})
print("test req: ", x.text)