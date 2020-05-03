with open("miniClusterPassata3Part2.txt", "r") as file:
    miniCluster = eval(file.readline())


for indexListaProdotti in range(len(miniCluster)):
    miniCluster[indexListaProdotti]=list(filter(lambda x: x[0]!='<page title>',miniCluster[indexListaProdotti]))
    print(miniCluster[indexListaProdotti])
with open("miniClusterFiltrato.txt", "w") as file:
    file.write(str(miniCluster))