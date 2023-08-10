library(RPostgres)

# Global parameters
startyr <- 2002
endyr   <- 2011 
outdir  <- "/kellogg/proj/jpj8711/crsp_dsf"

# Create a connection called "wrds"
wrds <- dbConnect(Postgres(),
                  host='wrds-pgdata.wharton.upenn.edu',
                  port=9737,
                  dbname='wrds',
                  sslmode='require',
                  user='hoffa')
# AT THIS POINT, EXPECT A DUO PUSH


# FUNCTION TO PULL ONE YEAR OF CRSP DAILY STOCK FILE
download_dsf <- function(year, outdir) {
  # Define a SELECT query
  query = "select cusip, permco, permno, date, prc, ret, numtrd, vol "
  query = paste(query, "from crsp.dsf ", sep="")
  query = paste(query, "where date >= '", year, "-01-01' and ", sep="")
  query = paste(query, "date <= '", year, "-12-31'", sep="")
  # query

  # Execute the select query
  res <- dbSendQuery(wrds, query)
  data <- dbFetch(res)

  outfile = paste("dsf",year,Sys.Date(),sep="_")
  outpath = paste(outdir, "/", sep="") 
  outpath = paste(outpath, outfile, ".csv", sep="")

  # Test for existence of outdir before attempting to write
  if (!dir.exists(outdir)) {
    dir.create(outdir)
  }
  
  write.csv(data, outpath, row.names=TRUE)
} #end download_dsf


# FUNCTION TO PULL ONE YEAR OF CRSP DSF linked with SECURITY INFO
download_dsfenhanced <- function(year, outdir) {
  # Define a SELECT query
  query = "select a.cusip, a.permco, a.permno, issuernm, ticker, date, prc, ret, numtrd, vol, securitytype "
  query = paste(query, "from crsp.dsf as a left join crsp.wrds_names_query as b ", sep="")
  query = paste(query, "on a.cusip = b.cusip and a.date >= b.secinfostartdt and a.date <= b.secinfoenddt ")
  query = paste(query, "where date >= '", year, "-01-01' and ", sep="")
  query = paste(query, "date <= '", year, "-12-31'", sep="")
  # query
  
  # Execute the select query
  res <- dbSendQuery(wrds, query)
  data <- dbFetch(res)
  
  outfile = paste("dsf_enhanced",year,Sys.Date(),sep="_")
  outpath = paste(outdir, "/", sep="") 
  outpath = paste(outpath, outfile, ".csv", sep="")
  
  # Test for existence of outdir before attempting to write
  if (!dir.exists(outdir)) {
    dir.create(outdir)
  }
  
  write.csv(data, outpath, row.names=TRUE)
} #end download_dsfenhanced

# Call the functions
for (i in startyr:endyr) {
  download_dsf(i, outdir)
}

download_dsfenhanced(2020, outdir)
  
# Clean up workspace
dbClearResult(res)