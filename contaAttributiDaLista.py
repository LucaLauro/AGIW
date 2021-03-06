#conto gli attributi uguali in una lista di file che viene passata
import json

def contaAttributiUguali(listaDiFile):
    dict={}
    for file in listaDiFile:
        path = 'data/' + file +".json"  # occhio all' estensione, non è presente nel csv
        f = open(path)
        data = json.load(f)
        for (k, v) in data.items():  # per ogni elemento nel json
            if k in dict:                # se la chiave(nome attributo del json) esiste nel dict aggiungi 1
                dict[k] = dict[k] + 1
            else:
                dict.update({k: 1})
        f.close()
    return dict
