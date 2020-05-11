import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from ottimizzazioneClusterName import ottimizzazioneGroundTruh
import json


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
with open("miniClusterOttimizzato.txt", "r") as file:
    cluster = eval(file.readline())
df = pd.read_csv("ground_truth/test50.csv")

# Scorro solo le coppie match
for index, row in df.iterrows():
   target_attribute = row['left_target_attribute']
   # Filtraggio della ground truth prima dell'esecuzione dell'algoritmo
   left_attribute = row['left_instance_attribute']
   right_attribute = row['right_instance_attribute']
   left_value = row['left_instance_value']
   right_value = row['right_instance_value']
   ldata = left_attribute.split("//")[2]
   rdata = right_attribute.split("//")[2]
   attributeNameList = set([ldata, rdata])
   fileNameList = [left_attribute, right_attribute]
   attributeValueList = set([left_value, right_value])
   if any(target_attribute in d for d in newCluster):
       for dictionary in newCluster:
           if target_attribute in dictionary.keys():
               #Dal momento che i valori di un dizionario non sono iterabili
               valori = list(dictionary.values())[0]
               # Uso un set così da scartare i duplicati
               newAttributeNameList = set().union(valori[0], attributeNameList)
               newAttributeValueList = set().union(valori[1], attributeValueList)
               newfileNameList = set().union(valori[2], fileNameList)
               dictionary[target_attribute] = (newAttributeNameList, newAttributeValueList, newfileNameList)
   else:
       newCluster.append({target_attribute: (attributeNameList, attributeValueList, fileNameList)})

productCluster = ottimizzazioneGroundTruh(cluster)
#[{brand:((brand,canon),{brand,manufacturer,...},{canon,...},{www.ebay.com/4274/brand,www.ebay.com/93785/brand...})}]


pozzo = [] #Cluster in cui vengono depositati tutti gli attributi che non si riesce ad accoppiare
#prima passata, valuto solo le chiavi uguali o uguali parzialmente

for d1 in productCluster:
    for key1, value1 in d1.items():
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
                    print(value2)
                    if fuzz.token_set_ratio(str1.replace("_"," "), str2.replace("_"," ")) > 65 and checkSimilarity(value1[0][1], value2[1]):
                        listaPossibilita.append(newCluster.index(d2))

        if len(str(key1))==1:  #mi capitano attributi con solo 1 lettera che fanno un bordello
            listaPossibilita=[]

        # HO PIU' POSSIBILITA' E PRENDO QUELLA CON IL PUNTEGGIO PIU' ALTO
        # listaPossibilita E' UNA LISTA DI INDICI
        if len(listaPossibilita)> 0:
            tuplePunteggi=[]
            for index in listaPossibilita:
                value2 = list(newCluster[index].values())[0]
                maxName = 0
                for nameAttribute in value2[0]:
                    i = fuzz.token_set_ratio(str(value1[0][0]), str(nameAttribute))
                    maxName= max(maxName,i)
                    #print(str(value1[0][0]),'----',str(nameAttribute))
                maxValue = 0
                for valueAttribute in value2[1]:
                    j = fuzz.token_set_ratio(str(value1[0][1]), str(valueAttribute))
                    if len(str(valueAttribute))>6 and len(str(valueAttribute).split(' '))<3:
                        j=j*2
                    maxValue=max(maxValue, j)
                    #print(str(value1[0][1]),'----', str(valueAttribute))
                media=maxName*4+maxValue*2
                tuplePunteggi.append((index,media))

            tuplaMax={"key2":0 }
            #print(tuplePunteggi)
            for tupla in tuplePunteggi:
                if tupla[1]>list(tuplaMax.values())[0]:
                    tuplaMax={tupla[0]:tupla[1]}
            if list(tuplaMax.values())[0]<400:
                print(tuplaMax)
                print(list(newCluster[list(tuplaMax.keys())[0]].values())[0])
                print(value1)

            # PARTE NUOVA: CONTROLLO DEGLI ATTRIBUTE NAME CHE STO ANDANDO AD INSERIRE
            key2 = list(newCluster[list(tuplaMax.keys())[0]].keys())[0]
            value2 = list(newCluster[list(tuplaMax.keys())[0]].values())[0]
            # Si controlla se questi attributi sono molto simili nel nome tra di loro. Uso come metro di giudizio la chiave del dizionario
            # process mi permette di creare una lista di tuple e da questa mi posso ricavare i nomi col punteggio più basso
            listOfScores = process.extract(key2,value2[0])
            print(listOfScores)
            for score in listOfScores:
                if score[1] < 55:
                    # Scorro il cluster della ground truth e vedo se ne trovo uno più adatto al seguente attributo. In caso positivo rimuovo
                    # l'attributo da value2
                    for d in newCluster:
                        key = list(d.keys())[0]
                        # Il confronto lo faccio con la chiave del dizionario
                        if fuzz.ratio(key,score[0]) > 80:
                            # Rimuovo l'elemento dal cluster e lo sposto in quello nuovo ma prima recupero il valore associato a quell'attributo
                            # Ci sono casi in cui il file non è definito ATTENZIONE
                            if value2[2]:
                                for file in value2[2]:
                                    find = False
                                   # Cerco nella stringa
                                   # Se il nome del file ha come delimitatore /  vedi caso di ebay (www.ebay.com/24539/screen size) bisogna trattarlo diversamente
                                    if len(file.split("//")) == 1: # sono nel caso con un solo /
                                        if file.split("/")[2] == score[0]:
                                            find = True
                                            producer = file.split("/")[0]
                                            product = file.split("/")[1]
                                    elif file.split("//")[2] == score[0] :
                                        find = True
                                        producer = file.split("//")[0]
                                        product = file.split("//")[1]
                                    if find:
                                        path = 'data/' + producer + '/' + product + ".json"  # carico il file del prodotto
                                        f = open(path)
                                        data = json.load(f)
                                        for (k, v) in data.items():
                                            if k == score[0]:
                                                # ho trovato il valore da rimuovere
                                                value2[1].remove(v)
                                                value2[0].remove(score[0])
                                                value2[2].remove(file)
                                                # modifico il cluster aggiungendo il nuovo valore appena recuperato
                                                value_to_modify = list(d.values())[0]
                                                attribute_name = value_to_modify[0].union({score[0]})
                                                attribute_value = value_to_modify[1].union({v})
                                                filename = value_to_modify[2].union({file})
                                                d[key] = (attribute_name, attribute_value, filename)
                                                break
                                        break
            attribute_name = value1[1].union(value2[0])
            attribute_value = value1[2].union(value2[1])
            filename = value1[3].union(value2[2])
            #print(filename)
            #print(d2[key2])
            newCluster[list(tuplaMax.keys())[0]][key2] = (attribute_name, attribute_value, filename)
            #print(newCluster[list(tuplaMax.keys())[0]])

        if not listaPossibilita :
            pozzo.append({key1: (value1[1], value1[2], value1[3])})


for elem in newCluster:
    print(elem)
#crea file di output
with open('ground_truth/manager8_output.txt', 'w') as file:
    for dictionary in newCluster:
        print(dictionary, file=file)
print("FATTO2")
print(len(newCluster))
print(newCluster)


#crea file per il pozzo
with open('ground_truth/pozzo8.txt', 'w') as file:
    for dictionary in pozzo:
        print(dictionary, file=file)
print("FATTO3")
print(len(pozzo))
print(pozzo)