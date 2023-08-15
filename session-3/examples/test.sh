#!/bin/bash

# load modules
module load python-miniconda3/4.12.0
module load R/4.3.0

# run scripts
python test.py
Rscript test.R

