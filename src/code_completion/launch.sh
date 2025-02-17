#!/bin/bash

total_workers=4
app_module="main:app"

for i in $(seq 1 $total_workers); do
    echo "Starting worker $i"
    if (( i % 4 == 1 )); then
        CUDA_VISIBLE_DEVICES=1 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --timeout=30 --bind 0.0.0.0:7861 $app_module 
    elif (( i % 4 == 2 )); then
        CUDA_VISIBLE_DEVICES=2 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --timeout=30 --bind 0.0.0.0:7862 $app_module 
    elif (( i % 4 == 3 )); then
        CUDA_VISIBLE_DEVICES=3 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --timeout=30 --bind 0.0.0.0:7863 $app_module 
    else
        CUDA_VISIBLE_DEVICES=0 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --timeout=30 --bind 0.0.0.0:7864 $app_module  
    fi
    sleep 1
done

wait