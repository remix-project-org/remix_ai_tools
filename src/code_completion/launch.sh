#!/bin/bash

total_workers=4
app_module="main:app"

for ((i=1; i<=4; i++)); do
    echo "Starting worker $i"
    if (( i % 4 == 1 )); then
        CUDA_VISIBLE_DEVICES=1 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --timeout=30 --bind 0.0.0.0:7861 --timeout 600 $app_module 
    elif (( i % 4 == 2 )); then
        CUDA_VISIBLE_DEVICES=2 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --timeout=30 --bind 0.0.0.0:7862 --timeout 600 $app_module 
    elif (( i % 4 == 3 )); then
        CUDA_VISIBLE_DEVICES=3 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --timeout=30 --bind 0.0.0.0:7863 --timeout 600 $app_module 
    else
        CUDA_VISIBLE_DEVICES=0 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --timeout=30 --bind 0.0.0.0:7864 --timeout 600 $app_module  
    fi
done

wait