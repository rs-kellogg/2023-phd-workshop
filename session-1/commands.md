# Graphical commands

## Quest Analytics Nodes

[Quest documentation](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest/)

## Software modules 

[Module documentation](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest-software-and-applications.html)

Example: load git module:

```bash
module avail git
module load git/2.37.2
```

Graphical tools available through modules:

- Stata: 
    ```bash
    module load stata/17; xstata-mp
    ```
- Python: 
    ```bash
    module load vscode/1.74.1; code
    ```
- R: 
    ```bash
    module load R/4.3.0; rstudio
    ```

## Juypyter Notebooks

```bash
module use --append /kellogg/software/Modules/modulefiles
module load miniconda/23.3.1
jupyter lab --browser=firefox
```
