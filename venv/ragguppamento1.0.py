import json

pippo=0
with open("miniCluster.txt", "r") as file:
    miniCluster = eval(file.readline())  #[[(_,[],[],[]),(_,[],[],[])..],[(_,[],[],[])]]
for prodottiUguali in miniCluster:
    for attributi in prodottiUguali:
        set1 = set(attributi[2][0].lower().split(' '))
        for attributiSuccessivi in prodottiUguali[prodottiUguali.index(attributi)+1:]:
            set2 = set(attributiSuccessivi[2][0].lower().split(' '))
            if len(set1)>2 and set1 == set2:
                pippo=pippo+1
                #print(set1)
                #print(set2)
print(pippo)




"""
prodottiUguali = miniCluster[0]
attributi=prodottiUguali[0]
attributi2=prodottiUguali[prodottiUguali.index(attributi)+1]
print(attributi)
print(attributi2)
print(prodottiUguali.index(attributi)+1)
print(type(attributi2[2][0]))"""








"""
s1 = 'abc def ghi'
s2 = 'def ghi abc'
set1 = set(s1.split(' '))
set2 = set(s2.split(' '))
print(set1 == set2)
print(len(set1))"""

