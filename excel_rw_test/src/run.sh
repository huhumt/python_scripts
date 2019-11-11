#!/usr/bin/env bash

cp ../test_output/2.8v/config.json ./
python3 main.py

cp ../test_output/3.0v/white/config.json ./
python3 main.py

cp ../test_output/3.0v/zebra/config.json ./
python3 main.py

cp ../test_output/3.3v/config.json ./
python3 main.py

cp ../test_output/3.5v/config.json ./
python3 main.py
