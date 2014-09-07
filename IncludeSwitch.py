import os 

lib_directory = "/Users/Tristan/Documents/Learning/Python/PythonFun"
extensions   = [".gls",".h"]

def get_common_elements( path, extensions ):
	file_extension_count = {}
	common_files = []
	for ext in extensions:
		for key in filter(lambda y: ext in y, os.listdir(path)):
			# remove extensions to find commonality 
			key = key.rsplit(".")[0]
			if key in file_extension_count:
			    file_extension_count[key] += 1
			else:
			    file_extension_count[key] = 1

			if file_extension_count[key] == len(extensions):
				common_files.append(key)

	return common_files

def modify_includes( file_path, file_name ):
	file_path = "".join([file_path,"/",file_name,".gls"])
	file_buffer = []
	with open( file_path,"r" ) as global_file:
		for line in global_file:
			if "#include" and file_name in line:
				file_buffer.append("\n")
			elif "#include" and ".gls" in line:
				global_to_header = line.partition(".gls")
				file_buffer.append(global_to_header[0] + ".h" + global_to_header[2])
			else:
				file_buffer.append(line)

	with open("temp1","w") as output_gls:
		for line in file_buffer:
			output_gls.write(line)

	file_path = file_path[:-4] + ".h"
	file_buffer = []

	with open( file_path, "r") as global_file:
		count_end_if = 0
		for line in global_file:
			file_buffer.append(line)
			if "#endif" in line:
				count_end_if = count_end_if + 1
		number_of_end_if = count_end_if
		count_end_if = 0

	with open("temp2","w") as output_h:
		for line in file_buffer:
			if "#endif" in line:
				count_end_if += 1
				if count_end_if == number_of_end_if:
					print "success"
					output_h.write('#include "' + file_name + '.h\"\n' + line)
				else:
					output_h.write(line)
			else:
				output_h.write(line)







for f in get_common_elements( lib_directory, extensions ):
	modify_includes( lib_directory, f )





