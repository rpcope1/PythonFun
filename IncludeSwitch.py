import os
#Use defaultdict to simplify code.
from collections import defaultdict
#Use sys to get args.
import sys

LIBRARY_DIRECTORY = "."
#Let's use a set literal.
EXTENSIONS = {".gls", ".h"}


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


def modify_includes(file_path, file_name):
    file_path = "".join([file_path, "/", file_name, ".gls"])
    file_buffer = []
    with open(file_path, "r") as global_file:
        for line in global_file:
            if "#include" and file_name in line:
                file_buffer.append("\n")
            elif "#include" and ".gls" in line:
                global_to_header = line.partition(".gls")
                file_buffer.append(global_to_header[0] + ".h" + global_to_header[2])
            else:
                file_buffer.append(line)

    with open("temp1", "w") as output_gls:
        for line in file_buffer:
            output_gls.write(line)

    file_path = file_path[:-4] + ".h"
    file_buffer = []

    with open(file_path, "r") as global_file:
        count_end_if = 0
        for line in global_file:
            file_buffer.append(line)
            if "#endif" in line:
                count_end_if = count_end_if + 1
        number_of_end_if = count_end_if
        count_end_if = 0

    with open("temp2", "w") as output_h:
        for line in file_buffer:
            if "#endif" in line:
                count_end_if += 1
                if count_end_if == number_of_end_if:
                    print "success"
                    output_h.write('#include "' + file_name + '.gls\"\n' + line)
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






