from provaClusterDict import clusterToDict

with open("miniClusterPassata4.txt", "r") as file:
    miniCluster = eval(file.readline())

dict = clusterToDict(miniCluster)
for indexElem in range(len(miniCluster)):
    for indexTupla in range(len(miniCluster[indexElem])):
        max_key = max(dict[indexElem][indexTupla][1], key=dict[indexElem][indexTupla][1].get)
        max_key=max_key.replace(' ','_')
        listAppoggio=list(miniCluster[indexElem][indexTupla])
        listAppoggio[0]=max_key
        miniCluster[indexElem][indexTupla]=tuple(listAppoggio)
with open("miniClusterOttimizzato.txt", "w") as file:
    file.write(str(miniCluster))