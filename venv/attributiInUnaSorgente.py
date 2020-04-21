import json
import os
import pandas
dict = {}
fileList = os.listdir("/Users/luca/PycharmProjects/agiw/venv/data/buy.net")
fileList.sort()
for file in fileList:
    path = '/Users/luca/PycharmProjects/agiw/venv/data/buy.net/'+file
    f = open(path)
    data = json.load(f)
    for (k, v) in data.items():   # per ogni elemento nel json
        if k in dict:              # se la chiave(nome attributo del json) esiste nel dict aggiungi 1
            dict[k] = dict[k]+1
        else:
            dict.update({k: 1})
    f.close()
print(dict)
