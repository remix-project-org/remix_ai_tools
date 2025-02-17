#!/bin/bash

total_workers=4
app_module="main:app"

CUDA_VISIBLE_DEVICES=1 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --bind 0.0.0.0:7861 --timeout 600 $app_module &&
CUDA_VISIBLE_DEVICES=2 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --bind 0.0.0.0:7862 --timeout 600 $app_module &&
CUDA_VISIBLE_DEVICES=3 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --bind 0.0.0.0:7863 --timeout 600 $app_module &&
CUDA_VISIBLE_DEVICES=0 SERVERTYPE=flask gunicorn --workers=7 --threads=20 --bind 0.0.0.0:7864 --timeout 600 $app_module &&
wait