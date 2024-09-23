#!/bin/bash

# Define the number of times you want to run the command
NUM_TIMES=300

# Define the command you want to run
COMMAND="echo 'Hello, World!'"

# Loop through and run the command
for ((i=1; i<=NUM_TIMES; i++))
do
    echo "Running iteration $i"
    python yaml_main_parallel.py -f exp_config_N-obj-test.yaml --n_objective
done
