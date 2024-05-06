#!/bin/bash

#PJM -L "rscunit=ito-b"
#PJM -L "rscgrp=ito-g-1"
#PJM -L "vnode=1"
#PJM -L "vnode-core=9"
#PJM -L "elapse=96:00:00"
#PJM -j
#PJM -X

source ~/.bashrc

export PATH="$HOME/miniconda3/envs/benchmark-visualizer/bin:$PATH"
export PYTHONPATH=.


python yaml_main_parallel.py --ito --starting_point 0 --fragment_size 100 --input_file hyperparameter_indexes.csv