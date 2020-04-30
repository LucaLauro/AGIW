#da usare con miniClusterIniziale.txt

with open("../miniClusterIniziale.txt", "r") as file:
    miniCluster = eval(file.readline())

indexDaRimuovere=[]

for indexListaAttributiProdottiUguali in range(len(miniCluster)):
    indexUsati=[]
    for indexAttributo in range(len(miniCluster[indexListaAttributiProdottiUguali])-1):
        set1 = set(miniCluster[indexListaAttributiProdottiUguali][indexAttributo][1][0][1].lower().split(' '))
        #print(set1)
        for indexAttributiSuccessivi in range(indexAttributo+1,len(miniCluster[indexListaAttributiProdottiUguali])):
            if indexAttributiSuccessivi not in indexUsati :
                listAttributiSuccessivo=miniCluster[indexListaAttributiProdottiUguali][indexAttributiSuccessivi][1]
                set2 = set(miniCluster[indexListaAttributiProdottiUguali][indexAttributiSuccessivi][1][0][1].lower().split(' '))
                if len(set1) == 1 and set1 == set2 and len(list(set1)[0]) > 4 or len(set1) > 2 and set1 == set2:
                    listAttributi = miniCluster[indexListaAttributiProdottiUguali][indexAttributo][1]
                    nuovaListaProdotti=listAttributi+listAttributiSuccessivo
                    listaAppoggio=list(miniCluster[indexListaAttributiProdottiUguali][indexAttributo])
                    listaAppoggio[1]=nuovaListaProdotti
                    miniCluster[indexListaAttributiProdottiUguali][indexAttributo]=tuple(listaAppoggio)
                    indexUsati.append(indexAttributiSuccessivi)
                    indexDaRimuovere.append((indexListaAttributiProdottiUguali,indexAttributiSuccessivi,indexAttributo))

print(indexDaRimuovere)
print(len(indexDaRimuovere))
print(miniCluster[1])

for tupla in indexDaRimuovere:
    miniCluster[tupla[0]][tupla[1]]=0
print(miniCluster[1])
for indexListaAttributiProdottiUguali in range(len(miniCluster)):
    miniCluster[indexListaAttributiProdottiUguali]=list(filter(lambda x : x!=0,miniCluster[indexListaAttributiProdottiUguali]))
print(miniCluster[1])
with open("../miniClusterRaggruppato.txt", "w") as file:
    file.write(str(miniCluster))


