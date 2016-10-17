import os
import argparse

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

def main():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_size",
                        help="""set train dataset size as len(data) * TRAIN_SIZE.
                        By default TRAIN_SIZE=0.6""",
                        type=float)
    
    parser.add_argument("--shuffle",
                        help="shuffle dataset before choosing samples",
                        action="store_true")
    
    parser.add_argument("--balanced",
                        help ="""get balanced dataset with an equal number of 
                        samples in each classes. By default train dataset will 
                        be unbalanced, at least with one sample from each class""",
                        action="store_true")    
        
    args = parser.parse_args()
    train_size = "" if not args.train_size else "--train_size {0}".format(args.train_size)
    shuffle = "" if not args.shuffle else "--shuffle"
    balanced = "" if not args.balanced else "--balanced"
    
    start = time.time()
    if os.system("python3 data/multiclass/split_data.py {0} {1} {2}".format(train_size, shuffle, balanced)) == 0:
        try:
            print(colored("Generating train and test datasets done", "green"))
        except Exception:
            print("Generating train and test datasets done")
        PrintTime(start)
    else:
        try:
            print(colored("Generating train and test datasets failed", "red"))
        except Exception:
            print("Generating train and test datasets failed")
        sys.exit(0)        
        
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
        
main()

        