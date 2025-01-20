#!/bin/bash

for i in {1..15}
do
  curl -X POST http://localhost:7861/ai/api/vulnerability_check\
       -H "Content-Type: application/json" \
       -d '{
             "prompt": "Your prompt here",
             "context": "Your context here",
             "stream_result": false,
             "max_new_tokens": 50,
             "temperature": 0.7,
             "top_k": 50,
             "top_p": 0.9,
             "repeat_penalty": 1.0,
             "frequency_penalty": 0.0,
             "presence_penalty": 0.0
           }' &
  sleep 0.1
done