#!/bin/bash


# load in stata
module load stata/17

# Call Stata and run the do-file with command-line arguments
stata-mp -b do nlswork_input.do $1


# to run the script
# source nlswork.sh 1976

