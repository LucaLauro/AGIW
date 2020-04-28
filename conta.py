import json
#conto gli attibuti per fare controllare la consistenza
with open("miniClusterRaggruppato.txt", "r") as file:
    minicluster = eval(file.readline())
with open("miniCluster2.txt", "r") as file:
    minicluster2 = eval(file.readline())
counter=0
counter2=0
counter3=0
counter4=0
for stessiProdotti in minicluster:
    for cluster in stessiProdotti:
    #print(minicluster[1][index][1], len(minicluster[1][index][1]))
    #print(minicluster2[1][index][1], len(minicluster2[1][index][1]))
        counter = counter+ len(cluster[1])
        counter2=counter2+1
print(counter)
print(counter2)

for stessiProdotti in minicluster2:
    for cluster in stessiProdotti:
        counter3 = counter3+ len(cluster[1])
        counter4=counter4+1
print(counter3)
print(counter4)
#print(minicluster[1])
#print(minicluster2[1][180])
#print(minicluster2[1][170])
#print(minicluster2[1][59])
#print(minicluster[1][59])
for clusterList in minicluster:
    #print(clusterList)
    for attribute in clusterList:
        #print(attribute)
        for cluster in attribute[1]:
            #print(cluster)
            if 'www.ebay.com/53228/model' in cluster[2]:
                print('ci sta', minicluster.index(clusterList),clusterList.index(attribute))
"""for list in miniCluster:
    for tupla in list:
        lunghezzaDiAndrea = lunghezzaDiAndrea+ len(tupla[3])
print(lunghezzaDiAndrea)
#print(miniCluster)"""
"""counter=0
for prodotti in prodottiUguali:
    for prodotto in prodotti:
        path = 'data/' + prodotto + ".json"
        f = open(path)
        data = json.load(f)
        for (k, v) in data.items():
            counter=counter+1
        f.close()
print(counter)"""