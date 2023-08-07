// Clear all previous data and results
clear all
set more off

// Call the reg_by_year function from the separate do-file
do "nlswork_input.do"

// Load test data
input str10 year float wage
"1976" 1000
"1976" 1200
"1977" 1100
"1977" 1300
"1978" 1050
"1978" 1250
"1979" 1150
"1979" 1350
end

// Call the reg_by_year function with the test data
reg_by_year wage if year == "1976", YEAR("1976")

// Verify the results
estimates table, cells(b se) nonumber noobs

