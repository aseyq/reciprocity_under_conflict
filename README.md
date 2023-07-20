# Reciprocity under conflict: Replication Materials

This repository provides all the materials necessary to replicate our study.

## Contents of this repository

The repository contains the following items:

- `code/simulation`: This directory contains the simulation code implemented in Python 3.
- `code/analysis`: This directory contains the code for the analysis and plots written in R.
- `output/`: This directory will contain the output for the simulation (data). 
- `plots/`: This directory will contain the plots generated by R.

## Data

There are two ways to reproduce the results of our study:

**1. Simulate the study on your machine**

You can reproduce our results by running the simulation code on your machine. Note that running the simulation code with every possible parameter combination may take considerable time. (Several days on a standard machine with eight cores). However, you can still run it with fewer iterations and without the robustness check parameters. Indeed default parameters in this repository are a reduced version. You can find those parameters in `code/simulation/simulate.py` and comment in the full parameter set.

**2. Use Our Precomputed Data**

We also provide the precomputed data that we used in our study, which you can download from the following link (805 MB in total): https://www.dropbox.com/sh/zu6czzbl1jiscmq/AACE0-A3NiDN2Q98zk9R6QQ9a?dl=0

## Instructions to Reproduce

To reproduce the analysis and plots presented in our study, you need to run the R scripts provided in the `code/` directory. These scripts use the data generated by the simulation code or the precomputed data, depending on the option you choose.

Note that you will need to install the necessary R packages listed in the `code/requirements.R` file before running the analysis scripts. 

The resulting plots and analysis will be saved in the `plots/` directory.

### Reproducing using our pre-simulated data
1- Clone the repository 
```
git clone https://github.com/aseyq/reciprocity_under_conflict.git
```

2- Download `.parquet` files from the Dropbox link (805 MB) and extract the `.parquet` files (`df_aggregate_payoffs.parquet`, `df_coop.parquet`, `df_long.parquet` in the folder `output/processeddata`
https://www.dropbox.com/sh/zu6czzbl1jiscmq/AACE0-A3NiDN2Q98zk9R6QQ9a?dl=0

Alternatively, you can use wget to download the files using command line to `output/processeddata`:
```
cd reciprocity_under_conflict
```

```
cd output/processeddata
```

```
wget "https://www.dropbox.com/scl/fi/62bn7bziqjq5k8spocf96/df_aggregate_payoffs.parquet?rlkey=bg5k5yddm3ln5ceza1c3y8qxk&dl=1" -O df_aggregate_payoffs.parquet
```

```
wget "https://www.dropbox.com/scl/fi/ob4bba2s41ao015l9cf4d/df_coop.parquet?rlkey=f5pbpps68i1u4lmzvm2qzpcib&dl=1" -O df_coop.parquet
```

```
wget "https://www.dropbox.com/scl/fi/z0ninjglk72kh4jiz0ds9/df_long.parquet?rlkey=y0zbhe0m37o0dr0nosmoevd1i&dl=1" -O df_long.parquet
```

4- Install the required R packages if necessary
```
# (go to the main folder `reciprocity_under_conflict` if you are not)
cd code/analysis
```

```
RScript requirements.R
```
5- Run the following scripts
  - Plots in the paper: `paper_plots
  - SI: `si_plots.R`, `si_basefit.R`, `si_moran.R`

```
Rscript paper_plots.R
```

```
Rscript si_plots.R
```

```
Rscript si_basefit.R
```

```
Rscript si_moran.R
```
  

### Reproducing by running the simulations
1- Clone the repository 
```
git clone https://github.com/aseyq/reciprocity_under_conflict.git
```
2- Go to the downloaded folder
```
cd reciprocity_under_conflict
```
3- (Optional but recommended) Create a Python virtual environment. This will let you install packages only in the virtual environment, in an isolated manner.
```
python3 -m venv venv
```
and activate it

(MacOS and Ubuntu)
```
source venv/bin/activate
```

(Windows)
```
venv\Scripts\activate
```
4- Install required packages

```
cd code/simulation
```

```
pip install -r requirements.txt
```

5- Run simulations 
Please note that it might take some time even with the default reduced number of parameters. 

The paper uses 1000 generations and 1000 iterations while the reproduction code has 300 generations and 12 iterations. This is sufficient to test to code but not to replicate the results. You set these numbers closer to original number of generations and iterations by modifying line 23 and 24 in `simulate.py`. 

```
python3 simulate.py
```

6- Combine CSV files created by the simulation (might take a couple of minutes)

```
cd code/analysis
```

```
Rscript 1_combine_csvs.R
```

This should combine the csv files generated by simulations and you should have `combined_data.csv` in `output/combineddata` foler.

7- Convert CSV files to a parquet file
```
Rscript 2_convert_parquet.R
```

This should convert csv file to parquet data which and create `combined.parquet` in `output/combineddata` folder.

8- Reshape data into a long format and generate additional tables (might take a couple of minutes)
```
Rscript 3_reshape_data.R
```

This should create `df_aggregate_payoffs.parquet`, `df_coop.parquet` and df_long.parquet` in the processed data folder `output/processeddata`. Then you can run the scripts to regenerate the analyses in the paper. At this point, you can delete the previous data generated and keep only the data in `processeddata` folder.

9- Go to `code/analysis` folder execute the following scripts to create plots in `plots/` folder. (Takes few minutes)
  - Plots in the paper: `paper_plots.R`
```
Rscript paper_plots.R
```


  - Plots in Supplementary Information: `si_plots.R`, `si_basefit.R`, `si_moran.R` (Note that you should have simulated also additional parameter set of robustness checks.
  
```
Rscript si_plots.R
```

```
Rscript si_basefit.R
```

```
Rscript si_moran.R
```

## System Requirements
### Hardware requirements
Any modern personal computer or server that supports Windows, MacOS, or Linux operating system with enough RAM (at least 4 GB recommended.) The original simulations take a long time and generate data around 2GBs. Some of the operations like combining the data files after the simulations might require larger RAM depending on the number of simulation parameters. But if you once convert it to parquet (or download the `parquet` files we provided), you wouldn't need to use a memory as big as the dataset as it uses Apache arrow (arrow) to solve this issue.

We tested this repository with a following machine:
Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz Processor
32,0 GB RAM




## Software Requirements
You need to have Python 3 (used 3.8) for simulations and R (used 4.2.3) for the analysis.

Additionally, we used the following packages (and their dependencies) which can be installed automatically using requirements files in the repository:

Python packages:
- Numpy 1.22
- Pandas 2.0.3
- joblib 1.3.1
- Pytest 6.2.5

R packages
- dplyr (1.1.0)
- purr (1.0.0)
- forcats (1.0.0)
- string (1.5.0)

We tested this repository on Windows 11 and Ubuntu 18

## Citation

If you use our materials for your own research, please cite our original paper using the following reference:

[TBA] 


