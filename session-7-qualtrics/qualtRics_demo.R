###########################
# Retrieving Qualtrics Results
############################

# Set Global Parameters
outdir = "downloads"  # specified as a relative path in working dir

# Clear Workspace
rm(list=ls()) 

# Install and load necessary libraries
if(!require("qualtRics")) install.packages("qualtRics")
if(!require("dplyr")) install.packages("dplyr")
if(!require("stringr")) install.packages("stringr")
if(!require("rmarkdown")) install.packages("rmarkdown")
if(!require("vtable")) install.packages("vtable")
if(!require("stargazer")) install.packages("stargazer")
if(!require("data.table")) install.packages("data.table")
if(!require("formattable")) install.packages("formattable")
if(!require("vcd")) install.packages("vcd")

library(qualtRics)
library(dplyr)
library(stringr)
library(rmarkdown)
library(vtable)
library(stargazer)
library(data.table)
library(formattable)
library(vcd)

## RUN THIS STEP FIRST TIME ONLY, TO GENERATE ".Renviron" FILE
#qualtrics_api_credentials(api_key = "INSERT YOUR API KEY HERE",
#                          base_url = "ca1.qualtrics.com",
#                          install = TRUE, 
#                          overwrite = TRUE)
readRenviron("~/.Renviron")

if (!dir.exists(outdir)) {
  dir.create(outdir)
}

# Show all surveys 
surveys   <- all_surveys()
surveys

# Select one project by name
myproject <- filter(surveys, name=="Response Pilot 2023 (Prolific)")
myproject
myproject$id[1]

#Fetch the survey for that project as .RDS file
mysurvey <- fetch_survey(surveyID = myproject$id[1],
                         save_dir = outdir,
                         force_request = TRUE,
                         verbose = TRUE)
nrow(mysurvey)

# save the approximate day/time of when you downloaded the survey
Sys.time()
download_time <- format(Sys.time(), "%a %b %d %X %Y")
download_message <- paste("The ", myproject$name, "survey data is called ", myproject$id[1] , ".rds and was downloaded on: ", download_time, sep="")
download_message

# save download time to log file
logfile_path <- paste(outdir, "/logfile.txt", sep="")
writeLines(download_message, logfile_path)

# Read RDS file into dataframe "mysurvey", and save copy as CSV
rdspath <- paste(outdir, "/", myproject$id[1], ".rds", sep="")
mysurvey <- readRDS(file = rdspath)
csvpath <- paste(outpath, "/", myproject$id[1], ".csv", sep="")
ret <- write.csv(x=mysurvey, file=csvpath)


# Fix problem of spaces in column names!
names(mysurvey) <- str_replace_all(names(mysurvey),c(" "=".", ","=""))
names(mysurvey)[names(mysurvey) == "Duration.(in.seconds)"] <- "Duration"
colnames(mysurvey)

### FILTERING
# Eliminate test responses
mysample <- filter(mysurvey, Q5 != "delete me")

# Function to return total respondents and % who are female
sample_count <- function(a) {
  females <- filter(a, Gender == "Female")
  pct_female <- (nrow(females) / nrow(a))
  return = paste("The sample now contains ", nrow(a), " reponses, ", percent(pct_female,1), " of which are from subjects who identify as female.", sep="", collapse=NULL) 
  return
}
sample_count(mysample)

# More filtering examples
# Did you pass the attention check?
mysample2 <- filter(mysample, Check == "eleven")
print("We removed anyone who failed the comprehension check.")
sample_count(mysample2)


# Three ways to eliminate outliers for response time
# (a) Using a hard cutoff...
print("We removed observations where total duration was greater than 5 minutes.")
mysample3a <- filter(mysample2, Duration < 300)
sample_count(mysample3a)

# (b) using quantiles...
quant_duration <- quantile(mysample$`Duration`, probs=seq(0,1,.05), na.rm=FALSE, names=FALSE)
quant_duration
mysample3b <- filter(mysample2,   `Duration` > quant_duration[2])
mysample3b <- filter(mysample3b, `Duration` < quant_duration[20])
sample_count(mysample3b)

# (c) using mean and standard deviation
print(mean(mysample2$Duration))
print(  sd(mysample2$Duration))
mysample3c <- filter(mysample2, `Duration` < mean(mysample2$Duration) + 1.645*sd(mysample2$Duration))
print("We removed responses that were more than 1.645 standard deviations beyond mean response time.")
sample_count(mysample3c)


