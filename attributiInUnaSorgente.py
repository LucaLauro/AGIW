# creo un dizionario dove la chiave è il nome dell'attributo e il valore è il valore è il numero delle occorrenze in una sorgente
import json
import os
import pandas
dict = {}
fileList = os.listdir("data/buy.net")
fileList.sort()
for file in fileList:
    path = 'data/buy.net/'+file
    f = open(path)
    data = json.load(f)
    for (k, v) in data.items():   # per ogni elemento nel json
        if k in dict:              # se la chiave(nome attributo del json) esiste nel dict aggiungi 1
            dict[k] = dict[k]+1
        else:
            dict.update({k: 1})
    f.close()
print(dict)
