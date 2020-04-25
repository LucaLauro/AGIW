import json
#conto gli attibuti per fare controllare la consistenza
with open("miniCluster2.txt", "r") as file:
    minicluster = eval(file.readline())
counter=0
for stessiProdotti in minicluster:
    for cluster in stessiProdotti:
        counter = counter+ len(cluster[1])
print(counter)
"""lunghezzaDiAndrea = 0
for list in miniCluster:
    for tupla in list:
        lunghezzaDiAndrea = lunghezzaDiAndrea+ len(tupla[3])
print(lunghezzaDiAndrea)
#print(miniCluster)"""
"""counter=0
for prodotti in prodottiUguali:
    for prodotto in prodotti:
        path = '/Users/luca/PycharmProjects/agiw/venv/data/' + prodotto + ".json"
        f = open(path)
        data = json.load(f)
        for (k, v) in data.items():
            counter=counter+1
        f.close()
print(counter)"""