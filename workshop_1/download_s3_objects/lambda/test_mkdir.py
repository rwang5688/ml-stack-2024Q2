# Python program to explain os.mkdir() method 

# importing os module 
import os 

# Parent Directory path 
parent_dir = "/tmp"
# Directory 
directory = "test_datasets"
# Path 
path = os.path.join(parent_dir, directory)
if os.path.exists(path) is False:
    # mode 
    mode = 0o755
    # Create the directory with mode
    os.mkdir(path, mode) 
    print("Directory '% s' created" % directory) 

# Parent Directory path 
parent_dir = "/tmp" + "/" + "test_datasets"
# Directory 
directory = "lab_01_churn"
# Path 
path = os.path.join(parent_dir, directory) 
if os.path.exists(path) is False:
    # mode 
    mode = 0o755
    # Create the directory with mode
    os.mkdir(path, mode) 
    print("Directory '% s' created" % directory)
