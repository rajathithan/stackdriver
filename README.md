 # Multiprocessing stackdriver log extraction to your local windows machine
 
 This script helps in extracting the logs faster from stackdriver. 
 
Checks for 
* gcloud installation,
* Current account
* Current project 

![Check pre-requisites](/ss/1.jpg)


Press Enter to start the query building

* Enter the start & end date and time format in yyyy-mm-dd hh:mm:ss format
* Enter the key - value pair for advanced filter

![Query builder](/ss/2.jpg)


* Press enter for adding more key-value pairs
* Enter 'q' from adding key-value pairs
* Finally the filter arguments are displayed for reference. 

![Query builder - additional arguments](/ss/3.jpg)

* Multiprocessing starts based on the number of cpu cores in your local system

![Multiprocessing](/ss/4.JPG)

* The extracted information is saved in .log format
* The contents of the log file will be in pretty printed Json format

![Log file](/ss/5.JPG)










