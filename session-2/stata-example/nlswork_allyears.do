clear
log using mylog.log, replace

// Load the "nlswork" dataset (if not already loaded)
use https://www.stata-press.com/data/r17/nlswork.dta

// Generate a table of interview counts by year
tabulate year, matcell(interview_counts)


// Write a function that can process any input year
capture program drop reg_by_year

program define reg_by_year
    syntax varlist [if] [in], YEAR(string) [Other Options]

     // Get the year from the command-line argument
    local year "`1'"

    // Subset the dataset by the specified year
    qui keep if year == `year'

    // Run fixed effects regression
    xtreg `varlist', fe `Other Options'

    // Generate the table title
    local table_title "Fixed Effects Reg by Year `year'"

    // Save regression results as a formatted table
    estout, title("`table_title'") cells(b(star fmt(%9.3f)) se(fmt(%9.3f))) replace
end



// Loop through all years
forval year = 1976/1982 {
    // Call the Stata function with the specified year
    reg_by_year wage if year == `year', YEAR("`year'")
}