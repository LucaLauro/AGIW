from fuzzywuzzy import fuzz
from numpy import nan
#with open("datiCompletiCompattati.txt", "r") as file:
#    pozzo = eval(file.readline())



"""
listClusterDict={}
for dict in pozzo:
    for k,d in dict.items():#tuple dei cluster
        if k in listClusterDict:
            listClusterDict[k]+=1
        else:
            listClusterDict.update({k : 1})
listClusterDict={k: v for k, v in reversed(sorted(listClusterDict.items(), key=lambda item: item[1]))}
print(listClusterDict)
print(len(listClusterDict))
"""


with open("ground_truth/pozzo_manager_output.txt", "r") as file:
    pozzo = eval(file.readline())
for elem in pozzo:
    print(elem)