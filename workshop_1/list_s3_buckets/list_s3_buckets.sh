#!/bin/bash

echo "[CMD] python lambda_handler.py"
cd lambda
python ./lambda_handler.py --task-spec ../$1
cd ..
