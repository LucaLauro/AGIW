from fuzzywuzzy import fuzz
from numpy import nan


def checkSimilarity(attribute_value, lista):
    for value in lista:
        limit = 65
        if len(attribute_value.split()) == 1 or len(attribute_value) < 8 and len(str(value).split()) == 1:
            limit = 84
        ratio = fuzz.ratio(str(attribute_value).lower(), str(value).lower())
        if ratio > limit:
            return True
    return False

newCluster = [] #Nuovo cluster
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterraggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("/Users/it059837/PycharmProjects/datarocket/datiCompletiCompattati.txt", "r") as file:
    productCluster = eval(file.readline())

with open("/Users/it059837/PycharmProjects/datarocket/ground_truth/pozzo_manager_output.txt", "r") as file:
    newCluster = eval(file.readline())


pozzo = [] #Cluster in cui vengono depositati tutti gli attributi che non si riesce ad accoppiare

#prima passata, valuto solo le chiavi uguali o uguali parzialmente

print(len(productCluster))
for d1 in productCluster:
    for key1, value1 in d1.items():
        print(productCluster.index(d1))
        listaPossibilita=[]
        for d2 in newCluster:
            for key2, value2 in d2.items():
                str1=str(key1)
                str2=str(key2)
                dataPD = str1.split('_')
                dataPD=list(filter(lambda x : len(str(x))>2, dataPD))
                dataPD=set(dataPD)
                dataGT=set(str2.split('_'))

                if str1 == str2 or str1 in str2 or str2 in str1 or len(dataPD.intersection(dataGT))>0:
                    if fuzz.token_set_ratio(str1.replace("_"," "), str2.replace("_"," ")) > 65 and checkSimilarity(value1[0][1], value2[1]):
                        listaPossibilita.append(newCluster.index(d2))

        if len(str(key1))==1:  #mi capitano attributi con solo 1 lettera che fanno un bordello
            listaPossibilita=[]
        # CASO 1: STESSA CHIAVE --> AGGIUNGO
        #if len(listaPossibilita)==1:   # mi mette troppo schifo nei cluster, devo introdurre una soglia minima per l'unione
         # #ci sta qualche problema in questa fase, dei dati spariscono magicamente
         #  value= list(newCluster[listaPossibilita[0]].values())[0]
         #   attribute_name = value1[1].union(value[0])
         #   attribute_value = value1[2].union(value[1])
         #   filename = value1[3].union(value[2])
         #   key=list(newCluster[listaPossibilita[0]].keys())[0]
         #   newCluster[listaPossibilita[0]][key] = (attribute_name, attribute_value, filename)

        # HO PIU' POSSIBILITA' E PRENDO QUELLA CON IL PUNTEGGIO PIU' ALTO
        # listaPossibilita E' UNA LISTA DI INDICI
        if len(listaPossibilita)> 0: #stessa cosa di sopra, devo introdurre una soglia
            tuplePunteggi=[]
            for index in listaPossibilita:
                value2 = list(newCluster[index].values())[0]
                maxName = 0
                for nameAttribute in value2[0]:
                    i = fuzz.token_set_ratio(str(value1[0][0]), str(nameAttribute))
                    maxName= max(maxName,i)
                maxValue = 0
                for valueAttribute in value2[1]:
                    j = fuzz.token_set_ratio(str(value1[0][1]), str(valueAttribute))
                    if len(str(valueAttribute))>6 and len(str(valueAttribute).split(' '))<3:
                        j=j*2
                    maxValue=max(maxValue, j)
                media=maxName*4+maxValue*2
                tuplePunteggi.append((index,media))

            tuplaMax={"key2":0 }
            for tupla in tuplePunteggi:
                if tupla[1]>list(tuplaMax.values())[0]:
                    tuplaMax={tupla[0]:tupla[1]}
            if list(tuplaMax.values())[0] > 350:
            #da controllare questa parte, sicuramente ho fatto casino con gli indici, devo usare gli indici e non d2 sennò sovrascrivo sempre
            #e non accumulo mai
                value2=list(newCluster[list(tuplaMax.keys())[0]].values())[0]
                attribute_name = value1[1].union(value2[0])
                attribute_value = value1[2].union(value2[1])
                filename = value1[3].union(value2[2])
                key2=list(newCluster[list(tuplaMax.keys())[0]].keys())[0]
                newCluster[list(tuplaMax.keys())[0]][key2] = (attribute_name, attribute_value, filename)

        if not listaPossibilita :
            pozzo.append({key1: (value1[0], value1[1], value1[2], value1[3])})

#crea file di output
with open('/Users/it059837/PycharmProjects/datarocket/ground_truth/prova_output.txt', 'w') as file:
    file.write(str(newCluster))
print("FATTO2")



#crea file per il pozzo
with open("/Users/it059837/PycharmProjects/datarocket/ground_truth/prova_pozzo.txt", "w") as file:
    file.write(str(pozzo))
print("FATTO3")
print(len(pozzo))
