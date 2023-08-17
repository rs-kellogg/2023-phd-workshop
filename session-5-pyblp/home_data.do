clear all

* Load the dataset
import delimited "ex_fes_homeprices.csv", clear

* Create a directory for output files
local output_dir "stata_results_`c(current_date)'"
mkdir "`output_dir'"

* Open a log file to save the results and timings
log using "`output_dir'/stata_regression_results.log", replace

* Set the panel data structure
xtset home_id

* Fixed effects regression with clustered standard errors using xtreg
timer clear
timer on 1
xtreg log_sale_price list_fsbo age_home new i.month year, fe cluster(home_id)
timer off 1
timer list 1

* Fixed effects regression with clustered standard errors using areg
timer clear
timer on 2
areg log_sale_price list_fsbo age_home new i.month year, absorb(home_id) cluster(home_id)
timer off 2
timer list 2

* Fixed effects regression with clustered standard errors using reghdfe
timer clear
timer on 3
reghdfe log_sale_price list_fsbo age_home new i.month year, absorb(home_id) vce(cluster home_id)
timer off 3
timer list 3

* Save the results 
log close

