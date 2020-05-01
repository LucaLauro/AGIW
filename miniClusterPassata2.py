#da usare con miniClusterPassata1.txt
#prendo come input il primo minicluster con i primi minicluster ragguppati(solo le coppie con attribute value e attribute name uguali sono state
#raggruppate in questo momento) e aumento i cluster raggruppando anche quelli con le parole degli attribute value con un ordine diverso
#(vengono presi in esame solo gli attribute value con una parola ma più lunga di 4 caratteri, e quelli con almeno 3 parole)

from mergeTuple import mergeTuple

with open("miniClusterPassata1.txt", "r") as file:
    miniCluster = eval(file.readline())


for indexListaProdotti in range(len(miniCluster)):
    indexUsati=[]                                 #uso un indice per memorizzare i valori che ho già raggruppato
    for indexAttributo in range(len(miniCluster[indexListaProdotti]) - 1):   #scansiono i file a coppie dove il primo è sempre in posizione precedente al secondo
        for indexAttributiSuccessivi in range(indexAttributo+1, len(miniCluster[indexListaProdotti])):
            if indexAttributiSuccessivi not in indexUsati and indexAttributo not in indexUsati:
                listAttributiSuccessivo=miniCluster[indexListaProdotti][indexAttributiSuccessivi][1]
                paroleClusterPrincipale = set(miniCluster[indexListaProdotti][indexAttributo][1][0][1].lower().split(' '))
                paroleClusterDaRaggruppare = set(miniCluster[indexListaProdotti][indexAttributiSuccessivi][1][0][1].lower().split(' '))
                if len(paroleClusterPrincipale) == 1 and paroleClusterPrincipale == paroleClusterDaRaggruppare and len(list(paroleClusterPrincipale)[0]) > 4 \
                        or len(paroleClusterPrincipale) > 2 and paroleClusterPrincipale == paroleClusterDaRaggruppare:
                    miniCluster=mergeTuple(miniCluster, indexListaProdotti, indexAttributo, indexAttributiSuccessivi)
                    indexUsati.append(indexAttributiSuccessivi)


for indexListaProdotti in range(len(miniCluster)):     #filtro i cluster sostituiti con 0(quelli che ho raggruppato)
    miniCluster[indexListaProdotti]=list(filter(lambda x : x != 0, miniCluster[indexListaProdotti]))

with open("miniClusterPassata2.txt", "w") as file:
    file.write(str(miniCluster))


