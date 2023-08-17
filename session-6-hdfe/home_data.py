import numpy as np
import pandas as pd
import os
import time
from fixedeffect.fe import fixedeffect

# Load the dataset
df = pd.read_csv('ex_fes_homeprices.csv')

# Create a directory for output files
output_dir = "Python_fe_" + time.strftime("%Y-%m-%d")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Perform FE regression with clustering
exog_x = ['list_fsbo', 'age_home', 'new']
y = ['log_sale_price']
category = ['home_id', 'month']
cluster = ['home_id']
model_fe = fixedeffect(data_df=df, dependent=y, exog_x=exog_x, category=category, cluster=cluster)
start_time_fe = time.time()
result_fe = model_fe.fit()
end_time_fe = time.time()

# Construct FE regression summary table
fe_summary = pd.DataFrame({
    "Coefficient": result_fe.params,
    "T-value": result_fe.tvalues,
    "P-value": result_fe.pvalues,
    "Standard Error": result_fe.bse
}, index=result_fe.params.index)

# Print FE regression summary
print("FE Regression Summary:")
print(fe_summary)

# Save FE regression summary to a CSV file
fe_summary_file = os.path.join(output_dir, "fe_regression_summary.csv")
fe_summary.to_csv(fe_summary_file)

# Calculate and print FE regression run time
fe_runtime = end_time_fe - start_time_fe
print("FE Regression Run Time:", fe_runtime, "seconds")

# Save run time information to a file
runtime_file = os.path.join(output_dir, "runtime.txt")
with open(runtime_file, "w") as f:
    f.write("FE Regression Run Time: {} seconds\n".format(fe_runtime))

print("Results saved to:", output_dir)

