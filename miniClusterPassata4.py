from bo import group_cluster_in_products
from mergeTuple import mergeTuple

with open("outMergeByName.txt", "r") as file:
    listMergeByName = eval(file.readline())
with open("miniClusterFiltrato.txt", "r") as file:
    miniCluster = eval(file.readline())


listaRaggruppamenti=group_cluster_in_products(listMergeByName)


for index in range(len(miniCluster)):
    for listElementiDaRaggruppare in listaRaggruppamenti[index]:
        elementoPrincipale=listElementiDaRaggruppare[0]
        if len(listElementiDaRaggruppare)>1:
            for elementoDaRaggruppare in listElementiDaRaggruppare[1:]:
                miniCluster=mergeTuple(miniCluster,index,elementoPrincipale,elementoDaRaggruppare)
for indexListaProdotti in range(len(miniCluster)):     #filtro i cluster sostituiti con 0(quelli che ho raggruppato)
    miniCluster[indexListaProdotti]=list(filter(lambda x : x != 0, miniCluster[indexListaProdotti]))


#with open("miniClusterPassata4.txt", "w") as file:
#    file.write(str(miniCluster))
for tuple in miniCluster[0]:
    print(tuple)