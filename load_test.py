
# In locust.py
from locust import HttpUser, task, constant, between
import random, requests
import json

class QuickstartUser(HttpUser):
    wait_time = between(max_wait=3, min_wait=1)
    host = "https://hkfll35zthu6e2-7861.proxy.runpod.net"

    @task
    def test_code_completion(self):
        self.client.post( "https://l70m88pijz3d0h-7860.proxy.runpod.net/ai/api/code_completion", 
        json={  # convert dictionary to string
            "context_code":"// SPDX-License-Identifier: GPL-3.0\n pragma solidity >=0.8.2 <0.9.0;\n\n\ncontract Storage {\n\n    uint256 number; \n\n    ///write a function for adding 2 uint256 numbers and return the result",
            "comment":"",
            "max_new_tokens":10
        })

    # @task
    # def test_code_generation(self):
    #     self.client.post( "https://l70m88pijz3d0h-7860.proxy.runpod.netai/api/code_completion", 
    #     json=json.dumps({
    #         "context_code":"// SPDX-License-Identifier: GPL-3.0\n pragma solidity >=0.8.2 <0.9.0;\n\n\ncontract Storage {\n\n    uint256 number; \n\n    ///write a function for adding 2 uint256 numbers and return the result",
    #         "comment":""
    #     }))


    # @task
    # def test_code_explaining(self):
    #     self.client.post( "https://l70m88pijz3d0h-7860.proxy.runpod.netai/api/code_explaining", 
    #     json=json.dumps({
    #         "context_code":"// SPDX-License-Identifier: GPL-3.0\n pragma solidity >=0.8.2 <0.9.0;\n\n/**\n * @title Storage\n * @dev Store & retrieve value in a variable\n * @custom:dev-run-script ./scripts/deploy_with_ethers.ts\n */\ncontract Storage {\n\n    uint256 number;",
    #     }))


    # @task
    # def test_error_explaining(self):
    #     self.client.post( "https://l70m88pijz3d0h-7860.proxy.runpod.netai/api/error_explaining", 
    #     json=json.dumps({
    #         "err":"ParserError: Expected pragma, import directive or contract/interface/library/struct/enum/constant/function/error definition.--> contracts/1_Storage.sol:42:5:"
    #     }))


    # @task
    # def test_contract_generation(self):
    #     self.client.post( "https://l70m88pijz3d0h-7860.proxy.runpod.netai/api/contract_generation", 
    #     json=json.dumps({
    #         "desc":"Write a contract for a simple storage"
    #     }))

    # @task
    # def test_answering(self):
    #     self.client.post( "https://l70m88pijz3d0h-7860.proxy.runpod.netai/api/answering", 
    #     json=json.dumps({
    #         "question":"What is the purpose of the storage contract?"
    #     }))
        
    def on_start(self):
        
        print('started')

x = requests.post("https://l70m88pijz3d0h-7860.proxy.runpod.net/ai/api/code_completion", 
        json={  # convert dictionary to string
            "context_code":"// SPDX-License-Identifier: GPL-3.0\n pragma solidity >=0.8.2 <0.9.0;\n\n\ncontract Storage {\n\n    uint256 number; \n\n    ///write a function for adding 2 uint256 numbers and return the result",
            "comment":"",
            "max_new_tokens":10
        })
print("test req: ", x.text)