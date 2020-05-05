from fuzzywuzzy import fuzz

with open("miniClusterPassata4.txt", "r") as file:
    miniCluster = eval(file.readline())
listClusterDict=[]
for listProdotto in miniCluster:
    listAppoggio=[]
    for tuple in listProdotto:#tuple dei cluster
        dictAppoggio = {}
        for elementi in tuple[1]:  #tuple all'interno di un cluster (brand,'canon','www.blablabla.com')
            if elementi[0] in dictAppoggio:
                dictAppoggio[elementi[0]]+=1
            else:
                dictAppoggio.update({elementi[0] : 1})
        listAppoggio.append((tuple[0],dictAppoggio))
    listClusterDict.append(listAppoggio)

dictTotale={}
for elem in listClusterDict:
    for tupla in elem:
        if tupla[0] in dictTotale:
            dictTotale[tupla[0]]+=1
        else:
            dictTotale.update({tupla[0] : 1})

for k,v in sorted(dictTotale.items()):
        print(k,v)
print(len(dictTotale))
#print(dictTotale)
"""
print(fuzz.token_sort_ratio('no','canon'))
print(fuzz.ratio('no','canon'))"""
