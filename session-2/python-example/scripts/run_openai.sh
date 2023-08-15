#bin/bash

# load some modules
module use --append /kellogg/software/Modules/modulefiles
module load git/2.37.2
module load curl/7.73.0
module load miniconda/23.3.1

# activate environment
conda activate openai-env

# go to the directory
cd ~/2023-phd-workshop/session-2/python-example/tests

# run the pipeline
openaihelper complete-prompts ${1} config.yml --outdir ${3} &
openaihelper complete-prompts ${2} config.yml --outdir ${3} &
wait
openaihelper validate-completions ${3} config.yml --outdir ${3}
upload-to-aws ${3} config.yml
send-to-slack ${3} config.yml


