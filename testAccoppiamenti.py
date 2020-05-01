from fuzzywuzzy import fuzz
from mergeTuple import mergeTuple

with open("miniClusterRaggruppato.txt", "r") as file:
    miniCluster = eval(file.readline())

listaIndexDaRaggruppare = []
for listaProdotti in miniCluster:
    for tuple in listaProdotti[:-1]:
        nomeAttibuto1 = tuple[0]
        tuplaValueMinuscolo = tuple[1][0][1].lower()
        index1 = listaProdotti.index(tuple)
        for tupleSuccessive in listaProdotti[listaProdotti.index(tuple):]:
            index2 = listaProdotti.index(tupleSuccessive)
            valoriDaVerificare = tupleSuccessive[1][0][1].lower()
            nomeAttibuto2 = tupleSuccessive[0]
            i = fuzz.token_sort_ratio(tuplaValueMinuscolo, valoriDaVerificare)
            i2 = fuzz.ratio(tuplaValueMinuscolo, valoriDaVerificare)
            # i3 = fuzz.token_set_ratio(tuplaValueMinuscolo, valoriDaVerificare)
            if i > 84 and i < 100 and index1 != index2 and nomeAttibuto1 != '<page title>' and not (
                    len(tuplaValueMinuscolo) < 7 and i2 < 50):
                listaIndexDaRaggruppare.append((miniCluster.index(listaProdotti), listaProdotti.index(tuple),
                                                listaProdotti.index(tupleSuccessive)))
                # print(i3)
    print(miniCluster.index(listaProdotti), '/191')

print(listaIndexDaRaggruppare)
"""
# listaIndexDaRaggruppare=[(indiceProdotto,indiceClusterProdottoPrincipale,indiceClusterProdottoDaRaggruppare)]
for indexTupla in range(len(listaIndexDaRaggruppare) - 1):
    clusterPrincipale = listaIndexDaRaggruppare[indexTupla][2]
    for indexTupleSuccessive in range(indexTupla + 1, len(listaIndexDaRaggruppare)):
        if listaIndexDaRaggruppare[indexTupleSuccessive][1] == clusterPrincipale:
            listaIndexDaRaggruppare[indexTupleSuccessive] = (listaIndexDaRaggruppare[indexTupleSuccessive][0], listaIndexDaRaggruppare[indexTupla][1],listaIndexDaRaggruppare[indexTupleSuccessive][2])

listaIndexDaRaggruppare=list( dict.fromkeys(listaIndexDaRaggruppare))

for indexTupla in range(len(listaIndexDaRaggruppare) - 1):
    clusterPrincipale = listaIndexDaRaggruppare[indexTupla][2]
    for indexTupleSuccessive in range(indexTupla + 1, len(listaIndexDaRaggruppare)):
        if listaIndexDaRaggruppare[indexTupleSuccessive][2] == clusterPrincipale:
            listaIndexDaRaggruppare[indexTupleSuccessive] = (listaIndexDaRaggruppare[indexTupleSuccessive][0], listaIndexDaRaggruppare[indexTupla][1],listaIndexDaRaggruppare[indexTupleSuccessive][1])
listaIndexDaRaggruppare=list( dict.fromkeys(listaIndexDaRaggruppare))
for tupla in listaIndexDaRaggruppare:
    miniCluster = mergeTuple(miniCluster, tupla[0], tupla[1], tupla[2])"""
with open("raggruppato.txt", "w") as file:
    file.write(str(listaIndexDaRaggruppare))
