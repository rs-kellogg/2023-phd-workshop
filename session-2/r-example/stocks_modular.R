#################################################
# Stock Price Analysis using Yahoo Finance Data
#################################################
rm(list=ls())

# Load libraries
library(quantmod)
library(ggplot2)

# Function to retrieve stock price data
get_stock_data <- function(ticker, start_date, end_date) {
  stock_data <- getSymbols(ticker, src = "yahoo", from = start_date, to = end_date, auto.assign = FALSE)
  closing_prices <- Cl(stock_data)
  data.frame(date = index(closing_prices), price = as.numeric(closing_prices))
}

# Function to plot stock price time series
plot_stock_price <- function(ticker, start_date, end_date) {
  stock_df <- get_stock_data(ticker, start_date, end_date)
  
  p <- ggplot(data = stock_df, aes(x = date, y = price)) +
    geom_line(color = "darkblue") +
    ggtitle(paste(ticker, "Stock Price Series")) +
    xlab("Date") +
    ylab("Price") +
    theme(plot.title = element_text(hjust = 0.5)) +
    scale_x_date(date_labels = "%b %y", date_breaks = "6 months")
  
  print(p)
}

# Function to save the plot as a PDF file
save_plot_as_pdf <- function(ticker, start_date, end_date) {
  stock_df <- get_stock_data(ticker, start_date, end_date)
  
  p <- ggplot(data = stock_df, aes(x = date, y = price)) +
    geom_line(color = "darkblue") +
    ggtitle(paste(ticker, "Stock Price Series")) +
    xlab("Date") +
    ylab("Price") +
    theme(plot.title = element_text(hjust = 0.5)) +
    scale_x_date(date_labels = "%b %y", date_breaks = "6 months")
  
  output_file <- paste(ticker, start_date, end_date, ".pdf", sep = "_")
  ggsave(filename = output_file, plot = p)
}

# Example usage
plot_stock_price("AMZN", "2013-01-01", "2017-06-01")
save_plot_as_pdf("AMZN", "2013-01-01", "2017-06-01")
