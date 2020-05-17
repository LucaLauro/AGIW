from numpy import nan

with open("ground_truth_fase_finale2.txt", "r") as file:
    ground_truth = eval(file.readline())
with open("out_finale3.txt", "r") as file:
    ultimaPassata = eval(file.readline())
with open("set_filename_ground_truth2.txt", "r") as file:
    setFilename = eval(file.readline())

true_positive=0
recall_denominatore=0
precision_denominatore=0
for index in range(len(ground_truth)):
    print(index)
    filenameNostri=list(ultimaPassata[index].values())[0][2]
    filenameGT=list(ground_truth[index].values())[0][2]
    true_positive= true_positive + len(filenameNostri.intersection(filenameGT))
    recall_denominatore=recall_denominatore+len(filenameGT)

    precision_denominatore=precision_denominatore+len((filenameNostri.difference(filenameGT)).intersection(setFilename))+len(filenameNostri.intersection(filenameGT))
    print(precision_denominatore)
precision=true_positive/precision_denominatore
recall=true_positive/recall_denominatore    #non so se escono int o double... da informarsi prima di eseguire


print(precision)
print(recall)
