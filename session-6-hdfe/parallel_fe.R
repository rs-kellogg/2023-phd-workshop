# Clean environment
rm(list=ls())

# Load required libraries
library(data.table)
library(lfe)
library(fixest)
library(parallel)

# Set the number of cores to use (adjust as needed)
num_cores <- 4

# Create a subfolder to store results
results_folder <- paste0("parallel_", format(Sys.Date(), "%Y%m%d"))
dir.create(results_folder, showWarnings = FALSE)

# Simulate a larger dataset with housing price data
set.seed(123)
n <- 5000
time_periods <- 10
n_entities <- 500
data <- data.table(
  entity = rep(1:n_entities, each = time_periods),
  time = rep(1:time_periods, times = n_entities),
  income = rnorm(n * time_periods),
  housing_price = rnorm(n * time_periods, mean = 500000, sd = 100000)
)

# Function to run fixed effects regression using felm
run_felm <- function(data) {
  library(lfe)
  model <- felm(housing_price ~ income | entity + time | 0 | entity, data = data)
  return(coef(model))
}

# Function to run fixed effects regression using feols
run_feols <- function(data) {
  library(fixest)
  model <- feols(housing_price ~ income + entity + time, data = data)
  return(coef(model))
}



# Split the data into chunks for parallel processing
chunks <- split(data, 1:num_cores)

# Parallelize fixed effects estimation using felm
cluster <- makeCluster(num_cores)
start_felm <- Sys.time ()
results_felm <- parLapply(cluster, chunks, run_felm)
elapse_felm <- Sys.time() - start_felm
print(elapse_felm)
cores_felm <- paste("felm cores", num_cores, sep=":")
print(cores_felm)
stopCluster(cluster)

# Parallelize fixed effects estimation using feols
cluster <- makeCluster(num_cores)
start_feols <- Sys.time ()
results_feols <- parLapply(cluster, chunks, run_feols)
elapse_feols <- Sys.time() - start_feols
print(elapse_feols)
cores_feols <- paste("feols cores", num_cores, sep=":")
print(cores_feols)
stopCluster(cluster)


# Combine results from parallel processing
combined_results_felm <- do.call(rbind, results_felm)
combined_results_feols <- do.call(rbind, results_feols)

# Save combined_results to a text file
output_file <- file.path(results_folder, "regression_results.txt")
sink(output_file, append = FALSE)
cat("Fixed Effects Estimation using felm:\n")
cat(combined_results_felm)
cat("\nFixed Effects Estimation using feols:\n")
cat(combined_results_feols)
sink()

# Save runtime information to a CSV file

runtime_df <- data.frame(
  Run_Time = c(elapse_felm, elapse_feols),
  Cores = c(cores_felm, cores_feols))
runtime_csv <- file.path(results_folder, "runtime.csv")
write.csv(runtime_df, file = runtime_csv, row.names = FALSE)

cat("All processing complete.\n")
