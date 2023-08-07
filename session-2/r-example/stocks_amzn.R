#################################################
# Stock Price Analysis using Yahoo Finance Data
#################################################
rm(list=ls())
# load libraries
library(quantmod)
library(ggplot2)

# Get stock price data
amzn <- getSymbols("AMZN", src = "yahoo", from = "2013-01-01", to = "2017-06-01", auto.assign = FALSE)

# Explore the data
head(amzn)
summary(amzn)


# Plot the time series graph
p = ggplot(data = amzn, aes(x = index(amzn), y = amzn[, "AMZN.Close"])) +
  geom_line(color = "darkblue") +
  ggtitle("Amazon Stock Price Series") +
  xlab("Date") +
  ylab("Price") +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_date(date_labels = "%b %y", date_breaks = "6 months")

# Save the plot as a PDF file
ggsave(filename = "amazon.pdf", plot = p)
