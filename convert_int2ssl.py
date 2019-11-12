import os

#this function goes through files with .int file extension
# and decomiles them
#int2ssl must be installed
def do_convert(script_directory):
    for file in os.listdir(script_directory):
        if file.endswith(".int"):
            os.system('int2ssl -1 f2_unpacked/scripts/{}'.format(file))


