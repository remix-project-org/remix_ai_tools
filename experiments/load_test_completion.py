
# In locust.py
from locust import HttpUser, task, constant, between
import random, requests
import json

url = "https://completion.remixproject.org"
no_rate_limit_url = "https://xofsxrwr8zkja6-7861.proxy.runpod.net/ai/api/"

class QuickstartUser(HttpUser):
    wait_time = between(min_wait=2, max_wait=20)
    host = no_rate_limit_url

    @task
    def test_code_completion(self):
        self.client.post(no_rate_limit_url+ "code_completion", 
        json={  "data":[# convert dictionary to string
            """// SPDX-License-Identifier: GPL-3.0
pragma solidity

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
     */""",
            "",
            False,
            50,
            1,
            0.9,
            50
        ]})

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
