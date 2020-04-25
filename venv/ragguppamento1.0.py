import json


clusterRaggruppato = []
with open("miniCluster.txt", "r") as file:
    miniCluster = eval(file.readline())  #[[(_,[],[],[]),(_,[],[],[])..],[(_,[],[],[])...]]
for prodottiUguali in miniCluster:
    tempListStessoProdotto = []
    for attributo in prodottiUguali:
        indexUtilizzati = []
        set1 = set(attributo[2][0].lower().split(' '))
        nonHoScritto = True
        for attributiSuccessivi in prodottiUguali[prodottiUguali.index(attributo)+1:]:
            set2 = set(attributiSuccessivi[2][0].lower().split(' '))
            if len(set1) == 1 and set1 == set2 and len(list(set1)[0]) > 4 and prodottiUguali.index(attributiSuccessivi) not in indexUtilizzati \
                    or len(set1) > 2 and set1 == set2 and prodottiUguali.index(attributiSuccessivi) not in indexUtilizzati :
                if nonHoScritto:
                    if attributo[1]==attributiSuccessivi[1] and attributo[2]==attributiSuccessivi[2]:
                        tempListStessoProdotto.append((attributo[0], attributo[1],
                                                       attributo[2],
                                                       attributo[3] + attributiSuccessivi[3]))
                        indexUtilizzati.append(prodottiUguali.index(attributiSuccessivi))
                        indexUtilizzati.append(prodottiUguali.index(attributo))
                        nonHoScritto = False
                    elif attributo[1]==attributiSuccessivi[1] and attributo[2]!=attributiSuccessivi[2]:
                        tempListStessoProdotto.append((attributo[0], attributo[1],
                                                       attributo[2] + attributiSuccessivi[2],
                                                       attributo[3] + attributiSuccessivi[3]))
                        indexUtilizzati.append(prodottiUguali.index(attributiSuccessivi))
                        indexUtilizzati.append(prodottiUguali.index(attributo))
                        nonHoScritto = False
                    elif attributo[2]==attributiSuccessivi[2] and attributo[1]!=attributiSuccessivi[1]:
                        tempListStessoProdotto.append((attributo[0], attributo[1] + attributiSuccessivi[1],
                                                       attributo[2],
                                                       attributo[3] + attributiSuccessivi[3]))
                        indexUtilizzati.append(prodottiUguali.index(attributiSuccessivi))
                        indexUtilizzati.append(prodottiUguali.index(attributo))
                        nonHoScritto = False
                else:
                    lst = list(tempListStessoProdotto[-1])
                    if attributiSuccessivi[1] not in lst[1] and attributiSuccessivi[2] not in lst[2]:
                        lst[1]=lst[1]+attributiSuccessivi[1]
                        lst[2]=lst[2]+attributiSuccessivi[2]
                        lst[3]=lst[3]+attributiSuccessivi[3]
                    elif attributiSuccessivi[1] in lst[1] and attributiSuccessivi[2] not in lst[2]:
                        lst[2] = lst[2] + attributiSuccessivi[2]
                        lst[3] = lst[3] + attributiSuccessivi[3]
                    elif attributiSuccessivi[1] not in lst[1] and attributiSuccessivi[2] in lst[2]:
                        lst[1] = lst[1] + attributiSuccessivi[1]
                        lst[3] = lst[3] + attributiSuccessivi[3]
                    elif attributiSuccessivi[1] in lst[1] and attributiSuccessivi[2] in lst[2]:
                        lst[3] = lst[3] + attributiSuccessivi[3]
                    t = tuple(lst)
                    tempListStessoProdotto[-1] = t
        if nonHoScritto and prodottiUguali.index(attributo) not in indexUtilizzati:
            tempListStessoProdotto.append(attributo)
    clusterRaggruppato.append(tempListStessoProdotto)
print(clusterRaggruppato)
lunghezzaDiAndrea = 0
for list in clusterRaggruppato:
    for tupla in list:
        lunghezzaDiAndrea = lunghezzaDiAndrea+ len(tupla[3])
print(lunghezzaDiAndrea)




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

