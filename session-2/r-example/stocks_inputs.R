#################################################
# Stock Price Analysis using Yahoo Finance Data
#################################################
rm(list=ls())
# load libraries
library(quantmod)
library(ggplot2)

# Function to plot stock price time series and save as PDF
plot_stock_price <- function(ticker, start_date, end_date) {

  # Get stock price data
  stock_data <- getSymbols(ticker, src = "yahoo", from = start_date, to = end_date, auto.assign = FALSE)
  
  # Extract closing prices
  closing_prices <- Cl(stock_data)
  
  # Create a data frame with date and closing prices
  stock_df <- data.frame(date = index(closing_prices), price = as.numeric(closing_prices))
  
  # Plot the time series graph
  p <- ggplot(data = stock_df, aes(x = date, y = price)) +
    geom_line(color = "darkblue") +
    ggtitle(paste(ticker, "Stock Price Series")) +
    xlab("Date") +
    ylab("Price") +
    theme(plot.title = element_text(hjust = 0.5)) +
    scale_x_date(date_labels = "%b %y", date_breaks = "6 months")
  
  # Construct output file name
  output_file <- paste(ticker, start_date, end_date, ".pdf", sep = "_")
  
  # Save the plot as a PDF file
  ggsave(filename = output_file, plot = p)
}

# Example usage
plot_stock_price("AMZN", "2013-01-01", "2017-06-01")
