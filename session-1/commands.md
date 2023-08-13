# KLC Software

## Quest Analytics Nodes

[Quest documentation](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest/)

## FastX Bookmarks

[FastX Browswe](https://www.kellogg.northwestern.edu/research-support/computing/kellogg-linux-cluster/connect.aspx)

## Modules 

[Module documentation](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest-software-and-applications.html)

### Example: load git module:

```bash
module avail git
module load git/2.37.2
```

### Additional KLC modules:

```bash
module use --append /kellogg/software/Modules/modulefiles
module avail miniconda
```

### Using Python/R/Stata with modules:

- Stata: ```module load stata/17```
    ```bash
    module load stata/17; xstata-mp # graphical
    ```
    ```bash
    module load stata/17; stata # command line
    ```
    
- Python: 
    ```bash
    module load vscode/1.74.1; code # graphical
    ```
    ```bash
    miniconda/23.3.1; python # command line
    ```
- R: 
    ```bash
    module load R/4.3.0; rstudio # graphical
    ```
    ```bash
    module load R/4.3.0; R # command line
    ```

## Juypyter Notebooks

```bash
module use --append /kellogg/software/Modules/modulefiles
module load miniconda/23.3.1
jupyter lab --browser=firefox
```
