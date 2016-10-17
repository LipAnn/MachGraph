import os

try:
    from termcolor import colored
except Exception:
    pass

import sys
import time

def PrintTime(start):
    try:
        print(colored("Time: {0} s".format(time.time() - start), "magenta"))
    except Exception:
        print("Time: {0} s".format(time.time() - start))
        
def PrintHelp():
    print("print --shuffle [train_size_percent=0.6] for shuffle data and get train dataset with size = len(data) * train_size_percent. Other samples will become a test dataset")
    print("then script will make project, launch it: fit on trainig set and predict on testing set and then compare predictions with real classes")


if "--help" in sys.argv or "-h" in sys.argv:
    PrintHelp()
    sys.exit(0)
    
if "--shuffle" in sys.argv:
    start = time.time()
    if len(sys.argv) == 3:
        os.system("python3 data/multiclass/split_data.py {0}".format(sys.argv[2]))
    else:
        os.system("python3 data/multiclass/split_data.py")
    try:
        print(colored("Shuffle done", "green"))
    except Exception:
        print("Suffle done")
    PrintTime(start)
    
start = time.time()
if os.system("make -C ./template") == 0:
    try:
        print(colored("Make done", "green"))
    except Exception:
        print("Make done")
    PrintTime(start)
else:
    try:
        print(colored("Make failed", "red"))
    except Exception:
        print("Make failed")
    sys.exit(0)
    
start = time.time()        
if os.system("./template/build/bin/task2 -d ./data/multiclass/train_labels.txt -m ./template/build/bin/model.txt --train") == 0:
    try:
        print(colored("Fit done", "green"))
    except:
        print("Fit done")
    PrintTime(start)
else:
    try:
        print(colored("Fit failed", "red"))
    except Exception:
        print("Fit failed")
    sys.exit(0)
    
start = time.time()        
if os.system("cd ./template/build/bin/ && ./task2 -d ../../../data/multiclass/test_labels.txt -m model.txt -l predictions.txt --predict") == 0:
    try:
        print(colored("Predict done", "green"))
    except Exception:
        print("Predict done")
    PrintTime(start)
else:
    try:
        print(colored("Predict failed", "red"))
    except Exception:
        print("Predict failed")
    sys.exit(0)
    

start = time.time()        
if os.system("cd ./template && python ./compare.py ../data/multiclass/test_labels.txt ./build/bin/predictions.txt") == 0:
    try:
        print(colored("Comparation done", "green"))
    except Exception:
        print("Comparation done")
    PrintTime(start)
else:
    try:
        print(colored("Comparation failed", "red"))
    except Exception:
        print("Comparation failed")
    sys.exit(0)

        