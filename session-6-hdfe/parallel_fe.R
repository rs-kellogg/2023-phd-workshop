# Load required libraries
library(data.table)
library(lfe)
library(fixest)
library(parallel)

# Set the number of cores to use (adjust as needed)
num_cores <- 4

# Simulate a dataset
set.seed(123)
n <- 1000
time_periods <- 10
n_entities <- 100
data <- data.table(
  entity = rep(1:n_entities, each = time_periods),
  time = rep(1:time_periods, times = n_entities),
  x = rnorm(n),
  y = rnorm(n) + 0.5 * x + rnorm(n)
)

# Function to run fixed effects regression using felm
run_felm <- function(data) {
  model <- felm(y ~ x | entity + time | 0 | entity, data = data)
  return(coef(model))
}

# Function to run fixed effects regression using feols
run_feols <- function(data) {
  model <- feols(y ~ x | entity + time | entity, data = data)
  return(coef(model))
}

# Split the data into chunks for parallel processing
chunks <- split(data, 1:num_cores)

# Parallelize fixed effects estimation using felm
cluster <- makeCluster(num_cores)
results_felm <- parLapply(cluster, chunks, run_felm)
stopCluster(cluster)

# Parallelize fixed effects estimation using feols
cluster <- makeCluster(num_cores)
results_feols <- parLapply(cluster, chunks, run_feols)
stopCluster(cluster)

# Combine results from parallel processing
combined_results_felm <- do.call(rbind, results_felm)
combined_results_feols <- do.call(rbind, results_feols)

# Print the combined results
print("Fixed Effects Estimation using felm:")
print(combined_results_felm)

print("Fixed Effects Estimation using feols:")
print(combined_results_feols)

