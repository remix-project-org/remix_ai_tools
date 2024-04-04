
# In locust.py
from locust import HttpUser, task, constant, between
import random, requests
import json

url = "https://solcoder.remixproject.org"
class QuickstartUser(HttpUser):
    wait_time = between(min_wait=10, max_wait=15)
    host = "https://solcoder.remixproject.org"

    @task
    def test_answering(self):
        self.client.post(url,# + "code_completion", 
        json={  "data":[# convert dictionary to string
            "What are modiers for in solitdity?",
            "solidity_answer",
            False,
            1000,
            0.9,
            0.92,
            50
        ]})

    @task
    def test_code_generation(self):
        self.client.post(url,# + "code_completion", 
        json={  "data":[# convert dictionary to string
            "Function for casting a user vote using the struct Vote",
            "code_completion",
            "",
            False,
            100,
            0.9,
            0.92,
            50
        ]})

    @task
    def test_code_explaining(self):
        self.client.post(url,# + "code_completion", 
        json={  "data":[# convert dictionary to string
            """
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract Storage {

    uint256 number;

    function store(uint256 num) public {
        number = num;
    }

    function retrieve() public view returns (uint256){
        return number;
    }
}
""",
            "code_explaining",
            False,
            2000,
            0.9,
            0.92,
            50
        ]})

        