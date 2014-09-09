import os
#Use defaultdict to simplify code.
from collections import defaultdict
#Use sys to get args.
import sys
#Use regex to find stuff in the file.as
import re

LIBRARY_DIRECTORY = "."
#Let's use a set literal.
EXTENSIONS = {".gls", ".h"}

TEMP_GLS_NAME = "temp.gls_"
TEMP_HEADER_NAME = "temp.h_"

#Use this template with basename substituted in using the format function to generate a regex for each file.
INCLUDE_HEADER_REGEX_TEMPLATE = "\s*#include\s+((<\s*{basename}.h\s*>)|(\"\s*{basename}.h\s*\"))"
INCLUDE_GLOBAL_LIB_REGEX_TEMPLATE = "\s*#include\s+((<\s*{basename}.gls\s*>)|(\"\s*{basename}.gls\s*\"))"
INCLUDE_ALL_GLOBALS_REGEX = "\s*#include\s+((<\s*[^>]+.gls\s*>)|(\"\s*[^\"]+.gls\s*\"))"
#TODO: Maybe we don't want to alter #includes in comments?

FS_SEPERATOR = "\\" if os.name in ['nt', 'os2'] else "/"  # If os.name is posix, java or riscos, use unix separator

def get_common_elements(path, extensions):
    """
        Take a library path and a set of extensions to filter on and
        return a list of all file basenames that exist with all of the
        extensions specified.
    """
    file_basename_ext_dict = defaultdict(set)
    #Could consolidate some of the below.
    dir_files = [os.path.splitext(f) for f in os.listdir(path)]
    [file_basename_ext_dict[file_basename].add(file_ext) for file_basename, file_ext in dir_files]
    #If we have the right extensions, the file will go in this list.
    return [file_basename for file_basename, file_exts in file_basename_ext_dict.items() if file_exts == extensions]


#Note: I tacked on the _ at the end so these don't get confused with existing files.
def modify_includes(dir_path, file_basename, new_global_libary_file="temp.gls_", new_header_file="temp.h_"):
    """
        For a given directory path (dir_path) and file_basename (file name without the extension),
        attempt to write new temporary files with the includes in the correct spot.
    """
    #TODO: Check to ensure this function now works correctly with #ifdef #endif for multiple includes in scripts.
    #TODO: Ensure all preprocessor directives for gls are inserted at head, and directives are inserted correctly
    #TODO: in correct place in header file, even if they weren't before.
    #This should work on all platforms now.
    file_path = FS_SEPERATOR.join([dir_path, "{}.gls".format(file_basename)])
    file_buffer = []
    with open(file_path, "r") as current_file:
        current_include_header_regex = INCLUDE_HEADER_REGEX_TEMPLATE.format(basename=file_basename)
        for line in current_file:
            #if "#include" and file_basename in line:  # Should be if "#include" in line and file_basename in line.
            #That doesn't do what you think it should. Regex is probably good here.
            if re.search(current_include_header_regex, line):
                file_buffer.append("\n")
            elif re.search(INCLUDE_ALL_GLOBALS_REGEX, line):
                global_to_header = line.partition(".gls")
                file_buffer.append(global_to_header[0] + ".h" + global_to_header[2])
            else:
                file_buffer.append(line)

    with open(new_global_libary_file, "w") as output_gls:
        output_gls.write("".join(file_buffer))

    file_path = FS_SEPERATOR.join([dir_path, "{}.h".format(file_basename)])
    file_buffer = []

    with open(file_path, "r") as global_file:
        count_end_if = 0
        for line in global_file:
            file_buffer.append(line)
            if "#endif" in line:
                count_end_if += 1
        number_of_end_if = count_end_if
        count_end_if = 0

    with open(new_header_file, "w") as output_h:
        for line in file_buffer:
            if "#endif" in line:
                count_end_if += 1
                if count_end_if == number_of_end_if:
                    print "success"
                    output_h.write('#include "' + file_basename + '.gls\"\n' + line)
                else:
                    output_h.write(line)
            else:
                output_h.write(line)


def modify_codebase_includes(codebase_directory, extensions):
    for f in get_common_elements(codebase_directory, extensions):
            modify_includes(codebase_directory, f)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            modify_codebase_includes(arg, EXTENSIONS)
    else:
        sys.stderr.write("Usage: {} (codebase directories)\n".format(sys.argv[0]))
        sys.stderr.write("Attempts to fix header/library relations (#include locations) for specified directory.")






