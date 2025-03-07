
# In locust.py
from locust import HttpUser, task, constant, between
import random, requests
import json

url = "http://solcodertest.org/"
no_rate_limit_url = "http://solcodertest.org/"

class QuickstartUser(HttpUser):
    wait_time = between(min_wait=2, max_wait=20)
    host = no_rate_limit_url

    @task
    def test_code_completion(self):
        self.client.post(no_rate_limit_url, 
            headers={"Content-Type": "application/json"},
            json={ 
            "prompt": "import numpy as np\nnp.",
            "context": "import numpy as np\n",
            "temperature": 0.0,
            "max_new_tokens": 100,
            "top_p": 0.9,
            "top_k": 50,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "repeat_penalty": 0.0,
            "stream": False,
            "ctxFiles": [],
            "currentFileName": "test_input.json"
        })

#     @task
#     def test_code_insertion(self):
#         self.client.post(no_rate_limit_url + "code_insertion", 
#         json={  "data":[# convert dictionary to string
#         """
# // SPDX-License-Identifier: GPL-3.0
# pragma solidity

# /**
#  * @title Storage
#  * @dev Store & retrieve value in a variable
#  * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
#  */
# contract Storage {

#     uint256 number;

#     /**
#      * @dev Store value in variable
#      * @param num value to store
#      */
   
#         """,
#         """
#     /**
#      *  @dev Retrieve stored value
#      */
#     function retrieve() public view returns (uint256) {
#         return number;
#     }

# }
#             """,
#             1024,
#             1,
#             0.9,
#             50
#         ]})
