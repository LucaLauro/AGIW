from numpy import nan
with open("ground_truth_fase_finale.txt", "r") as file:
    GT = eval(file.readline())

setFilename=set()

for elem in GT:
    print(GT.index(elem))
    for key1, value1 in elem.items():
        setFilename=setFilename.union(value1[2])
with open("set_filename_ground_truth.txt", "w") as file:
    file.write(str(setFilename))