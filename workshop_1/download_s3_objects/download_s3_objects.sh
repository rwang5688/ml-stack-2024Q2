#!/bin/bash

echo "[CMD] python main.py"
cd lambda
python ./lambda_handler.py --task-spec ../$1
cd ..
