import os
import json
with open("csvToListOfList.txt", "r") as file:
    listOfList = eval(file.readline())
fileDaScartare=flat_list = [item for sublist in listOfList for item in sublist]

clusterini=[]
listSorgenti=os.listdir('data')
for sorgente in listSorgenti:
    print(sorgente)
    listFile=os.listdir('data/'+sorgente)
    for file in listFile:
        path = 'data/'+sorgente+'/'+ file
        fileToCheck=sorgente+"/"+file
        if fileToCheck.replace(".json","") not in fileDaScartare:
            f = open(path)
            data = json.load(f)
            for (k, v) in data.items():
                k=str(k)
                if '(more than' in v:  # elimino i (more than xx%) che danno fastidio
                    i = v.index('(')
                    v = v[:i]
                if type(v) == list:
                    v = str(v).strip('[]')
                if k!='<page title>':
                    clusterini.append({k:((k,v),{k},{v},{path.replace(".json","")+"/"+k})})
with open("clusterRimanenti.txt", "w") as file:
    file.write(str(clusterini))

