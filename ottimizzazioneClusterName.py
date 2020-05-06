from provaClusterDict import clusterToDict
"""
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
"""
#[{brand:((brand,canon),{brand,manufacturer,...},{canon,...},{www.ebay.com/4274/brand,www.ebay.com/93785/brand...})}]
def ottimizzazioneGroundTruh(miniCluster):
    listProduct =[]
    for product in miniCluster:
        for tuple in product:
            dictAppoggio={}
            setName=set()
            setValue=set()
            setFile=set()
            bestTupla= list(filter(lambda x: x[0].replace('_',' ')==tuple[0].replace("_"," "), tuple[1]))[0]
            bestTuplaFix=(bestTupla[0],bestTupla[1])
            #for elem in tuple[1]:
             #   if elem[0]==tuple[0]:
            #      bestTupla=(elem[0],elem[1])
            #        break
            for elem in tuple[1]:
                setName.add(elem[0])
                setValue.add(elem[1])
                setFile.add(elem[2])
            dictAppoggio.update({tuple[0] : (bestTuplaFix,setName,setValue,setFile)})
            listProduct.append(dictAppoggio)
   return listProduct
