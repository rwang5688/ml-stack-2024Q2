#!/bin/bash

echo "[CMD] python main.py"
cd lambda
python ./main.py --task-spec ../$1
cd ..
