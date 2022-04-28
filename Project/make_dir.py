import os

directory = "C:\\Users\\Public\\Libraries\\"
extend = "\\"
dir_name = "Keylogger_python"
path = os.path.join(directory, dir_name)
try:
    os.makedirs(path, exist_ok = True)
    print("Directory Created")
except OSError as error:
    print("Directory exists")

file_path = path + extend
