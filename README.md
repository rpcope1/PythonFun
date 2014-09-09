IncludeSwitch.py <br/>
	- uses sample.h and sample.gls<br/>
	- finds common files in directory<br/>
		- commonality is defined as same file name different extension<br/>
		- get_common_elements was made slightly modular<br/>
			- takes in list of extensions<br/>
	- modify_includes was the goal of this script<br/>
		- removes .gls includes in .gls file<br/>
		- removes self.h include in self.gls file<br/>
		- adds self.gls include to bottom of self.h file

NOTE: The intent of this script may seem perplexing through the eyes of a C coder.
	  This was done to get around wonkiness in a test environment I was working
	  in. No information pertaining to the environment is given or apparent in 
	  the code. 
