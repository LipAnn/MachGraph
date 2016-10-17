import os, sys
from random import shuffle

train_size = 0.6
if len(sys.argv) > 1:
    train_size = float(sys.argv[1])
    
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

for key in classes:
    shuffle(classes[key])

train_pictures = []
test_pictures = []
for key in classes:
    size = len(classes[key])
    train_pictures.append((key, classes[key][:int(size * train_size)]))
    test_pictures.append((key, classes[key][int(size * train_size):]))
    
fout = open("./data/multiclass/train_labels.txt", "w")
for (label, paths) in train_pictures:
    for path in paths:
        print(path, label, file=fout)
        
fout.close()
fout = open("./data/multiclass/test_labels.txt", "w")

for (label, paths) in test_pictures:
    for path in paths:
        print(path, label, file=fout)

fout.close()