from bo import group_cluster_in_products
from mergeTuple import mergeTuple
with open("raggruppato.txt", "r") as file:
    listaRaggruppamenti = eval(file.readline())
with open("miniClusterRaggruppato.txt", "r") as file:
    miniCluster = eval(file.readline())

listaConUnSenso=group_cluster_in_products(listaRaggruppamenti)


for index in range(len(miniCluster)):
    for listElementiDaRaggruppare in listaConUnSenso[index]:
        elementoPrincipale=listElementiDaRaggruppare[0]
        for elementoDaRaggruppare in listElementiDaRaggruppare[1:]:
            print(index,elementoPrincipale,elementoDaRaggruppare)
            print(listaConUnSenso[6])
            miniCluster=mergeTuple(miniCluster,index,elementoPrincipale,elementoDaRaggruppare)
with open("testUltimoRaggruppamento.txt", "w") as file:
    file.write(str(miniCluster))