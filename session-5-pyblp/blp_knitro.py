import numpy as np
import pandas as pd
import pyblp
import knitro

# Load product and agent data
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

# Create the Problem instance
problem = pyblp.Problem(
    product_formulations=product_formulations,
    product_data=product_data,
    agent_formulation=agent_formulation,
    agent_data=agent_data,
    costs_type='log'
)

# Set initial values for sigma (random coefficient covariance matrix) and pi (mean of random coefficients)
initial_sigma = np.diag([3.612, 0, 4.628, 1.818, 1.050, 2.056])
initial_pi = np.c_[[0, -43.501, 0, 0, 0, 0]]

# Configure the optimization procedure using Knitro
optimization = pyblp.Optimization("knitro")
optimization.tol = 1e-6

# Solve the problem using Knitro
results = problem.solve(
    initial_sigma,
    initial_pi,
    costs_bounds=(0.001, None),
    W_type='clustered',
    se_type='clustered',
    initial_update=True,
    optimization=optimization
)

# Print the estimation results
print(results)
