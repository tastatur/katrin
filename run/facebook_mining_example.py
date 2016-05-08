#!/usr/bin/env python
import sys

from katrin.miners.facebook_miner import FacebookMiner, FacebookFriendsMinerConfig

if __name__ == "__main__":
    test_miner_config = FacebookFriendsMinerConfig()
    test_miner_config.load("katrin.ini")
    facebook_miner = FacebookMiner(test_miner_config)
    facebook_miner.mine(sys.argv[1])
