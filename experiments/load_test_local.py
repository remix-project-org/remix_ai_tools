
# In locust.py
import random, requests
import time
import threading, os
import json  # import json module


def make_request():
    start = time.time()
    res = requests.post("https://hkfll35zthu6e2-7860.proxy.runpod.net/ai/api/code", 
        json={  "data":[ # convert dictionary to string
            "// SPDX-License-Identifier: GPL-3.0\n pragma solidity >=0.8.2 <0.9.0;\n\n\ncontract Storage {\n\n    uint256 number; \n\n    ///write a function for adding 2 uint256 numbers and return the result\n",
            "",
            False,
            20,
            1,
            0.9,
            50
        ]})
    end = time.time()

    print(str(threading.get_ident()), " - Time taken:", end-start)
    print(res.text)

if __name__ == "__main__":
    threads = list()
    test_start = time.time()
    n_requests = 1000
    for i in range(n_requests):
        x = threading.Thread(target=make_request, args=())
        x.start()
        threads.append(x)
        time.sleep(0.1)
        if i%5 == 0:
            print("_________________________________________________________\n")
            time.sleep(5)

    for index, thread in enumerate(threads):
        thread.join()
    test_end = time.time()
    print("Total test time taken:", test_end-test_start)
    print("Average time per request:", (test_end-test_start)/n_requests)
