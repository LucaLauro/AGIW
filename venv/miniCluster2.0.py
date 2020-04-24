import json

with open("csvToListOfList.txt", "r") as file:
    prodottiUguali = eval(file.readline())
tupleList = []
for prodotti in prodottiUguali:
    clusterListStessiProdotti = []
    for prodotto in prodotti:
        path = '/Users/luca/PycharmProjects/agiw/venv/data/' + prodotto + ".json"
        f = open(path)
        data = json.load(f)
        for (k, v) in data.items():
            bool = False
            for tupla in clusterListStessiProdotti:
                if k in tupla[1] and v in tupla[2]:
                    tupla[3].append(prodotto + '/' + k)
                    bool = True
            if not bool:
                if type(v)==list:
                    v=str(v).strip('[]')
                clusterListStessiProdotti.append((k, [k], [v], [prodotto + "/" + k]))
    tupleList.append(clusterListStessiProdotti)


with open("miniCluster.txt", "w") as file:
    file.write(str(tupleList))
"""attributiTotali = 0
attributiNuovi = 0
for tuple in tupleList:
    for tupla in tuple:
        attributiTotali=attributiTotali+len(tupla[3])
        attributiNuovi = attributiNuovi+1
print(attributiNuovi,attributiTotali)"""