#!/usr/bin/env bash

find ./xlsx_data -name "*result_output*" | xargs rm -f
find ./xlsx_data -name "*.png*" | xargs rm -f
find ./xlsx_data -name "*.log*" | xargs rm -f

analysis_array=("analysis1" "analysis2" "analysis3")
config_array=( \
    "2.8V_zebral/config.json" \
    "3.0V/zebral/config.json" \
    "3.0V/white/config.json" \
    "3.3V_zebral/config.json" \
    "3.5V_zebral/config.json" \
    )

for item in ${analysis_array[*]}
do
    for ix in ${!config_array[*]}
    do
        target_config="./xlsx_data/$item/${config_array[$ix]}"
        if [ -f $target_config ]
        then
            cp $target_config ./config.json
            log_name=$(echo $target_config | sed -e "s#config.json#output.log#g")
            python3 ./src/main.py | tee $log_name
            printf "\n\n\t\t\t------------------------------------------Log file has been save to %s" $log_name
        fi
    done
done

rm ./config.json
