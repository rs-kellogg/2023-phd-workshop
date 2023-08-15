#bin/bash
cd ~/2023-phd-workshop/session-2/python-example/tests
openaihelper count-tokens ${1} config.yml --outdir ${2}
openaihelper complete-prompts ${1} config.yml --outdir ${2}
openaihelper validate-completions ${1} config.yml --outdir ${2}
convert-to-parquet ${1} config.yml --outdir ${2}
upload-to-aws ${1} config.yml --outdir ${2}
send-to-slack ${1} config.yml --outdir ${2}


