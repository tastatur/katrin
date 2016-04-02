#!/bin/bash

cd /miner/run
export PYTHONPATH=/miner:/miner/run:/miner/katrin

sleep 90
python3 ./facebook_mining_example.py ${SUSPECT}