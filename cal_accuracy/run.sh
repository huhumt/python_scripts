#!/usr/bin/env bash

python_path="E:\workmate\pgq\get_average\Python37\python"

rm -fr ./image/generate_img
mkdir ./image/generate_img

rm -fr ./image/target_img
mkdir ./image/target_img

$python_path ./src/main.py | tee "test.log"

$python_path ./src/read_log.py | tee "err.log"

./image/merge_2img.sh
mv ./image/generate_img/*_new.png ./image/target_img/
