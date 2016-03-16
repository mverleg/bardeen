
Changes
-----------


* 10 nov 2014: store and load functions for string, with compression, max age and directory creation
* 10 nov 2014: all load functions in storage now take an optional max_age, IOAgeError is raied if the file is expired
* 10 nov 2014: all save functions in storage now create the directory if it does not exist


