from bo import group_cluster_in_products
from mergeTuple import mergeTuple
with open("raggruppatoDaAndrea.txt", "r") as file:
    listaRaggruppamenti = eval(file.readline())
with open("miniClusterPassata2.txt", "r") as file:
    miniCluster = eval(file.readline())


for index in range(len(miniCluster)):
    for listElementiDaRaggruppare in listaRaggruppamenti[index]:
        elementoPrincipale=listElementiDaRaggruppare[0]
        if len(listElementiDaRaggruppare)>1:
            for elementoDaRaggruppare in listElementiDaRaggruppare[1:]:
                print(index,elementoPrincipale,elementoDaRaggruppare)
                print(listaRaggruppamenti[6])
                miniCluster=mergeTuple(miniCluster,index,elementoPrincipale,elementoDaRaggruppare)
for indexListaProdotti in range(len(miniCluster)):     #filtro i cluster sostituiti con 0(quelli che ho raggruppato)
    miniCluster[indexListaProdotti]=list(filter(lambda x : x != 0, miniCluster[indexListaProdotti]))
with open("miniClusterPassata3Part2.txt", "w") as file:
    file.write(str(miniCluster))