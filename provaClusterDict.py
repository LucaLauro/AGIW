from collections import Counter
with open("miniClusterPassata3Part2.txt", "r") as file:
    miniCluster = eval(file.readline())


def mergeDict(dict1, dict2):
    ''' Merge dictionaries and keep values of common keys in list'''
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = [value, dict1[key]]

    return dict3

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

for dict in listClusterDict:
    print(dict)
print(len(listClusterDict))
listClusterDict2=[]
indexUsati=[]
for indexTupla in range(len(listClusterDict)-1):
    for indexTuplaSuccessiva in range(indexTupla+1,len(listClusterDict)):
        if indexTupla not in indexUsati and indexTuplaSuccessiva not in indexUsati:
            if listClusterDict[indexTupla][0]==listClusterDict[indexTuplaSuccessiva][0]:
                #xx = Counter(listClusterDict[indexTupla][1])
                #yy = Counter(listClusterDict[indexTuplaSuccessiva][1])
                #xx.update(yy)
                #print(xx)
                #sum=dict(xx)
                print(listClusterDict[indexTupla])
                print(listClusterDict[indexTuplaSuccessiva])
                listClusterDict2.append((listClusterDict[indexTupla][0],mergeDict(listClusterDict[indexTupla][1],listClusterDict[indexTuplaSuccessiva][1])))
                indexUsati.append(indexTuplaSuccessiva)
print(listClusterDict2)
#[[(brand,{brand:48,manufacturer:2}),(model,{mpn:28,model:39}),...]]