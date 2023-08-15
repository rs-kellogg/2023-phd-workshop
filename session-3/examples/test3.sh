#!/bin/bash
. /etc/bashrc

# load modules
module load python-miniconda3/4.12.0

# run scripts
python test.py {$1}


