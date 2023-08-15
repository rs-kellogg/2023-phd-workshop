#!/bin/bash
# Our custom function
cust_func(){
  for i in {1..5}
  do
      echo "hello from $1 function call"
      sleep 1
  done
}
    
cust_func first & # Put a function in the background
cust_func second & # Put a function in the background
cust_func third & # Put a function in the background
cust_func fourth & # Put a function in the background
cust_func fifth & # Put a function in the background

 
## Put all cust_func in the background and bash 
## would wait until those are completed 
## before displaying all done message
wait 
echo "All done"
