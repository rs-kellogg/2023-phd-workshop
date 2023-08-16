#################
# BLP Optimizers
#################

# libraries
import numpy as np
import pandas as pd
import pyblp
import knitro
import os
import time
import sys
import argparse

############
# Inputs
############
parser = argparse.ArgumentParser(description='Estimate BLP using optimization methods.')
parser.add_argument("--opt_method", default="nfxp", help="optimization method")
args = parser.parse_args()
optimization_method = args.opt_method

# product and agent data
product_data = pd.read_csv(pyblp.data.BLP_PRODUCTS_LOCATION)
agent_data = pd.read_csv(pyblp.data.BLP_AGENTS_LOCATION)

# Define product formulations
product_formulations = (
    pyblp.Formulation('1 + hpwt + air + mpd + space'),
    pyblp.Formulation('1 + prices + hpwt + air + mpd + space'),
    pyblp.Formulation('1 + log(hpwt) + air + log(mpg) + log(space) + trend')
)

# Define agent formulation
agent_formulation = pyblp.Formulation('0 + I(1 / income)')

##############
# Functions
##############

# create output directory
def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

# select optimization method
def select_optimization_method(optimization_method):
    if optimization_method == "knitro":
        optimization = pyblp.Optimization(optimization_method)
        optimization.tol = 1e-6
    elif optimization_method == "bfgs":
        optimization = pyblp.Optimization(optimization_method)
        # Add any specific configuration for BFGS optimization here
    else:
        optimization = None  # Use default optimization method
    return optimization

##############
# To Run
############### 

def main(optimization_method, product_data, agent_data, product_formulations, agent_formulation):
    directory_name = f"{time.strftime('%Y-%m-%d')}_{optimization_method}"
    create_directory(directory_name)

    output_file = os.path.join(directory_name, 'output.txt')
    sys.stdout = open(output_file, 'w')

    problem = pyblp.Problem(
        product_formulations=product_formulations,
        product_data=product_data,
        agent_formulation=agent_formulation,
        agent_data=agent_data,
        costs_type='log'
    )

    initial_sigma = np.diag([3.612, 0, 4.628, 1.818, 1.050, 2.056])
    initial_pi = np.c_[[0, -43.501, 0, 0, 0, 0]]

    optimization = select_optimization_method(optimization_method)

    start_time = time.time()
    results = problem.solve(
        initial_sigma,
        initial_pi,
        costs_bounds=(0.001, None),
        W_type='clustered',
        se_type='clustered',
        initial_update=True,
        optimization=optimization
    )
    end_time = time.time()

    print(results)
    runtime = end_time - start_time
    print(f"\nRuntime: {runtime:.2f} seconds", file=sys.stdout)

if __name__ == "__main__":
    main(optimization_method, product_data, agent_data, product_formulations, agent_formulation)
