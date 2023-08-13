# Graphical commands

## Common modules 
module use --append /kellogg/software/Modules/modulefiles
module load git/2.37.2


- Stata: 
    ```bash module load stata/17; xstata-mp```
- Python: 
    ```bash module load vscode/1.74.1; code```
- R: 
    ```bash module load R/4.3.0; rstudio```

## Juypyter Notebooks

```bash
module load miniconda/23.3.1
jupyter lab --browser=firefox
```
