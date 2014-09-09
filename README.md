IncludeSwitch.py
	-uses sample.h and sample.gls
	-finds common files in directory
		-commonality is defined as same file name different extension
		-get_common_elements was made slightly modular
			-takes in list of extensions
	-modify_includes was the goal of this script
		-removes .gls includes in .gls file
		-removes self.h include in self.gls file
		-adds self.gls include to bottom of self.h file

NOTE: The intent of this script may seem perplexing through the eyes of a C coder.
	  This was done to get around wonkiness in a test enironment I was working
	  in. No information pertaining to the environment is
	  given or apparent in the code. 
