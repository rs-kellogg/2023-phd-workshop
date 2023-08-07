clear
log using mylog.log, replace

// Load the "nlswork" dataset (if not already loaded)
use https://www.stata-press.com/data/r17/nlswork.dta

// Generate a table of interview counts by year
tabulate year, matcell(interview_counts)

// Create a formatted table using estout
estout matrix(interview_counts, fmt(%10.0f) noobs) using "NLSWork Interviews by Year.txt", title("NLSWork Interviews by Year") replace

// Subset the dataset for the year 1976
keep if year == 76

// Run fixed effects regression for the year 1976
xtreg wage, fe
estout, title("Fixed Effects Reg by Year 1976") cells(b(star fmt(%9.3f)) se(fmt(%9.3f))) replace

// Subset the dataset for the year 1978
use https://www.stata-press.com/data/r17/nlswork.dta, clear
keep if year == 78

// Run fixed effects regression for the year 1978
xtreg wage, fe
estout, title("Fixed Effects Reg by Year 1978") cells(b(star fmt(%9.3f)) se(fmt(%9.3f))) replace
