# clean 
rm(list=ls())

# libraries

library(data.table)
library(lfe)
library(fixest)

# Read a csv file in R
data <- read.csv('ex_fes_homeprices.csv', header = TRUE, sep = ',')

# Function to create a subfolder and return its path
create_subfolder <- function(base_folder, folder_name) {
  subfolder_path <- file.path(base_folder, folder_name)
  
  if (!file.exists(subfolder_path)) {
    dir.create(subfolder_path)
  }
  
  return(subfolder_path)
}

# Function to run regression and measure time
run_regression <- function(model_name, formula, data) {
  start_time <- proc.time()
  model <- eval(parse(text = model_name))
  result <- model(formula, data = data)
  end_time <- proc.time()
  
  elapsed_time <- end_time - start_time
  
  return(list(result = result, elapsed_time = elapsed_time))
}

# Function to save regression results as a text file
save_as_text <- function(result, model_name, subfolder_path) {
  table_name <- file.path(subfolder_path, paste0(model_name, "_", format(Sys.Date(), "%Y%m%d"), ".txt"))
  capture.output(print(result), file = table_name)
}

# Define regression specifications
regressions <- list(
  #list(model = "lm", formula = log_sale_price ~ list_fsbo + age_home + new + as.factor(month) + year + as.factor(home_id)),
  list(model = "felm", formula = log_sale_price ~ list_fsbo + age_home + new + as.factor(month) + year | home_id | 0 | home_id),
  list(model = "feols", formula = log_sale_price ~ list_fsbo + age_home + new + as.factor(month) + year | home_id)
)

# Create a data.table to store time details
time_details <- data.table(Model = character(0), "CPU Time" = numeric(0), "Real Time" = numeric(0))

# Define base folder for subfolders
base_folder <- getwd()  # Change this to the desired base folder path

# Create a subfolder with the current date or use an existing one
subfolder <- create_subfolder(base_folder, format(Sys.Date(), "%Y%m%d"))

# Loop through regressions and run/save results
for (reg in regressions) {
  model_name <- reg$model
  formula <- reg$formula
  
  # Run regression and measure time
  regression_info <- run_regression(model_name, formula, data)
  result <- regression_info$result
  elapsed_time <- regression_info$elapsed_time
  
  # Save regression results as a text file
  save_as_text(result, model_name, subfolder)
  
  # Data check to confirm file was saved
  if (file.exists(file.path(subfolder, paste0(model_name, "_", format(Sys.Date(), "%Y%m%d"), ".txt")))) {
    cat("File saved successfully:", model_name, "\n")
  } else {
    cat("File could not be saved:", model_name, "\n")
  }
  
  # Store time details in data.table
  time_details <- rbind(time_details, data.table(Model = model_name, "CPU Time" = elapsed_time["user.self"], "Real Time" = elapsed_time["elapsed"]))
}

# Save time details as a CSV file
csv_file_name <- file.path(subfolder, paste0("regression_times_", format(Sys.Date(), "%Y%m%d"), ".csv"))
fwrite(time_details, csv_file_name)


