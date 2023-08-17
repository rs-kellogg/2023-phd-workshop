############################################
# Fixed Effects in Python on home sales data
############################################
# to tun this file on 4 cores please type:
# parallel_fe.py --cores 4

# load libraries
import numpy as np
import pandas as pd
import os
import time
import multiprocessing
from fixedeffect.fe import fixedeffect
import argparse

##########
# Inputs
##########

parser = argparse.ArgumentParser(description="Run FE regressions in parallel")
parser.add_argument("--cores", type=int, default=1, help="Number of cores to use for parallel processing")
args = parser.parse_args()

# Load the dataset
df = pd.read_csv('ex_fes_homeprices.csv')

###########
# Functions
###########

def create_output_directory():
    output_dir = "parallel_" + time.strftime("%Y-%m-%d") + "_python_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def save_summary_to_csv(summary_df, output_dir, filename):
    summary_file = os.path.join(output_dir, filename)
    summary_df.to_csv(summary_file)

def construct_fe_summary(result_fe):
    fe_summary = pd.DataFrame({
        "Coefficient": result_fe.params,
        "T-value": result_fe.tvalues,
        "P-value": result_fe.pvalues,
        "Standard Error": result_fe.bse
    }, index=result_fe.params.index)
    return fe_summary

def run_fe_regression(df, exog_x, y, category, cluster):
    model_fe = fixedeffect(data_df=df, dependent=y, exog_x=exog_x, category=category, cluster=cluster)
    result_fe = model_fe.fit()
    return result_fe

########
# Run
########

def main():
    # Create a directory for output files
    output_dir = create_output_directory()

    # Perform FE regression with clustering
    exog_x = ['list_fsbo', 'age_home', 'new']
    y = ['log_sale_price']
    category = ['home_id', 'month']
    cluster = ['home_id']

    num_processes = args.cores
    if num_processes <= 0:
        print("Invalid number of cores.")
        return

    # Parallelize FE regression using multiprocessing
    pool = multiprocessing.Pool(processes=num_processes)
    start_time_fe = time.time()
    results = pool.starmap(run_fe_regression, [(df, exog_x, y, category, cluster)] * num_processes)
    pool.close()
    pool.join()
    end_time_fe = time.time()

    # Construct FE regression summary table
    fe_summary = construct_fe_summary(results[0])

    # Print FE regression summary
    print("FE Regression Summary:")
    print(fe_summary)

    # Save FE regression summary to a CSV file
    save_summary_to_csv(fe_summary, output_dir, "fe_regression_summary.csv")

    # Calculate and print FE regression run time
    fe_runtime = end_time_fe - start_time_fe
    print("FE Regression Run Time:", fe_runtime, "seconds")

    # Save run time information to a file
    runtime_file = os.path.join(output_dir, "runtime.txt")
    with open(runtime_file, "w") as f:
        f.write("FE Regression Run Time: {} seconds\n".format(fe_runtime))

    print("Results saved to:", output_dir)

if __name__ == "__main__":
    main()

