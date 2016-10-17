import os, sys
import random
import argparse

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
    train_size = 0.6 if not args.train_size else args.train_size
    shuffle = args.shuffle
    balanced = args.balanced
    
    txt_files = list(filter(lambda x : x.endswith(".txt"), os.listdir("./data/multiclass")))
    
    if len(txt_files) == 1:
        os.system("mv ./data/multiclass/{0}".format(txt_files[0]) + " ./data/multiclass/all_pictures.txt")
    
    fin = open("./data/multiclass/all_pictures.txt")
    pictures_and_labels = [i.strip().split() for i in fin.readlines()]
        
    classes = dict()
    for (path, label) in pictures_and_labels:
        if label not in classes:
            classes[label] = [path]
        else:
            classes[label].append(path)
    
    if shuffle:
        for key in classes:
            random.shuffle(classes[key])
    
    train_pictures = []
    test_pictures = []
    if balanced:
        for key in classes:
            size = len(classes[key])
            for path in classes[key][:int(size * train_size)]:
                train_pictures.append((key, path))
            for path in classes[key][int(size * train_size):]:
                test_pictures.append((key, path))
        random.shuffle(train_pictures)
        random.shuffle(test_pictures)
    else:
        almost_all = []
        
        for key in classes:
            train_pictures.append((key, classes[key][0]))
            for path in classes[key][1:]:
                almost_all.append((key, path))
                
        random.shuffle(almost_all)
        size = int(len(almost_all) * train_size)
        train_pictures += almost_all[:size]
        test_pictures += almost_all[size:]
            
        
    fout = open("./data/multiclass/train_labels.txt", "w")
    for (label, path) in train_pictures:
        print(path, label, file=fout)
            
    fout.close()
    fout = open("./data/multiclass/test_labels.txt", "w")
    
    for (label, path) in test_pictures:
        print(path, label, file=fout)
    
    fout.close()
    
main()