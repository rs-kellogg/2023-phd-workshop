#!/bin/bash
. /etc/bashrc

# load modules
module load python-miniconda3/4.12.0

# run scripts
cd /kellogg/proj/wkt406/repos/2023-phd-workshop/session-3/examples/
python ./test.py {$1}


