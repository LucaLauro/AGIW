with open("miniClusterPassata3Part2.txt", "r") as file:
    miniCluster = eval(file.readline())


print(miniCluster[0])
listClusterDict=[]

for tuple in miniCluster[0]:#tuple dei cluster
    dictAppoggio = {}
    if tuple[0]!='<page title>':
        for elementi in tuple[1]:  #tuple all'interno di un cluster (brand,'canon','www.blablabla.com')
            if elementi[0] in dictAppoggio:
                dictAppoggio[elementi[0]]+=1
            else:
                dictAppoggio.update({elementi[0] : 1})
        listClusterDict.append((tuple[0],dictAppoggio))
print(listClusterDict)
print(len(listClusterDict))


#[[(brand,{brand:48,manufacturer:2}),(model,{mpn:28,model:39}),...]]