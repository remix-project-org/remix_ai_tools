
# In locust.py
from locust import HttpUser, task, constant, between
import random, requests
import json

url = "https://completion.remixproject.org"
class QuickstartUser(HttpUser):
    wait_time = between(min_wait=2, max_wait=5)
    host = "https://completion.remixproject.org"

    @task
    def test_code_completion(self):
        self.client.post(url,# + "code_completion", 
        json={  "data":[# convert dictionary to string
            "// SPDX-License-Identifier: GPL-3.0\n pragma solidity",
            "code_completion",
            "",
            False,
            10,
            1,
            0.9,
            50
        ]})

        
x = requests.post(url,#+ "code_completion", 
        json={  "data":[# convert dictionary to string
            "// SPDX-License-Identifier: GPL-3.0\n pragma solidity",
            "code_completion",
            "",
            False,
            10,
            1,
            0.9,
            50
        ]
        }, headers={"Content-Type": "application/json"})
print("test req: ", x.text)