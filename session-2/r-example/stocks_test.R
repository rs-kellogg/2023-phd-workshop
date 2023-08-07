rm(list=ls())

# Load libraries
library(testthat)
library(quantmod)
library(ggplot2)

# Load the functions from the source file
source("stocks_modular.R")

# Define unit tests for the functions
test_that("get_stock_data returns correct data frame", {
  stock_df <- get_stock_data("AMZN", "2013-01-01", "2017-06-01")
  expect_is(stock_df, "data.frame")
  expect_true(all(names(stock_df) %in% c("date", "price")))
  expect_true(nrow(stock_df) > 0)
})

test_that("plot_stock_price generates correct plot", {
  # Run the function and capture the plot object
  stock_plot <- capture.output(plot_stock_price("AMZN", "2013-01-01", "2017-06-01"))
  
  # Check if the plot object is not empty
  expect_true(length(stock_plot) > 0)
})

test_that("save_plot_as_pdf saves plot as PDF file", {
  # Generate a temporary file name for testing
  temp_file <- tempfile(fileext = ".pdf")
  
  # Run the function to save the plot
  save_plot_as_pdf("AMZN", "2013-01-01", "2017-06-01", output_file = temp_file)
  
  # Check if the file exists
  expect_true(file.exists(temp_file))
  
  # Delete the temporary file
  unlink(temp_file)
})

# Run the unit tests
test_file("stocks_test.R")
