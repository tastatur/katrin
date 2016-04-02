#!/bin/bash

cp -R ../../katrin tmp/
cp -R ../../run tmp/
docker build -t facebookminer .