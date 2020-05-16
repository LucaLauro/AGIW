import pandas as pd
from fuzzywuzzy import fuzz
from ottimizzazioneClusterName import ottimizzazioneGroundTruh
from nltk.corpus import wordnet


# QUESTA NUOVA VERSIONE CERCA DI UNIRE IL MANAGER 4 E 5
# 1: NON SI CREANO DEI NUOVI CLUSTER - SI USANO SOLO I CLUSTER GIA' CREATI DELLA GROUND TRUTH
# 2: GLI ATTRIBUTI CHE NON VENGONO ACCOPPIATI VENGONO BUTTATI IN UN NUOVO CLUSTER


def checkSimilarity(attribute_value, attribute_name,valueList, nameList):
    maxName = 0
    for nameAttribute in nameList:
        i = fuzz.token_set_ratio(attribute_name, str(nameAttribute))
        maxName = max(maxName, i)
        # print(str(value1[0][0]),'----',str(nameAttribute))
    maxValue = 0
    for valueAttribute in valueList:
        j = fuzz.token_set_ratio( attribute_value, str(valueAttribute))
        if len(str(valueAttribute)) > 4 and len(str(valueAttribute).split(' ')) < 3:
            j = j * 3
        maxValue = max(maxValue, j)
        # print(str(value1[0][1]),'----', str(valueAttribute))
    media = maxName * 2 + maxValue * 3
    # Considero che il nome abbia un valore superiore al 75 e lo stesso l'attributeValue: 75*2+75*3 = 375
    if media > 450:
        return True
    return False




newCluster = [] #Nuovo cluster
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterraggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("miniClusterOttimizzato.txt", "r") as file:
    cluster = eval(file.readline())
df = pd.read_csv("ground_truth.csv/ground_truth_random_reducedx2.csv")

for index, row in df.iterrows():
   target_attribute = row['left_target_attribute']
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

#ADESSO SI PROCEDE AL CONFRONTO FRA DIZIONARI: IL DIZIONARIO DELLA GROUND TRUTH E QUELLO DEI PRODOTTI
for d1 in productCluster:
    #SCORRO TUTTO IL CLUSTER DEI PRODOTTI
    for key1, value1 in d1.items():
        for d2 in newCluster:
            findOne = False
            for key2, value2 in d2.items():
            # CASO 1 E CASO 2 SONO STATI UNIFICATI IN QUESTO MODO:r
                if key1 == key2 or key1 in key2 or key2 in key1:
                    most_comment_values = value1[0]
                    common_value = most_comment_values[1]
                    if checkSimilarity(key1,common_value,value2[1],value2[0]):
                        # unisci cluster
                        for tupla in value1:
                            attribute_name = value1[1].union(value2[0])
                            attribute_value = value1[2].union(value2[1])
                            filename = value1[3].union(value2[2])
                        d2[key2] = (attribute_name, attribute_value, filename)
                        findOne = True
                        break
            else:
                continue
            break

        # NON HO TROVATO CIO' CHE VERCATO. Adesso aggiungo nel dizionario pozzo
        if not findOne:
            pozzo.append({key1: (value1[1], value1[2], value1[3])})


#crea file di output
with open('ground_truth.csv/final_output6.txt', 'w') as file:
    for dictionary in newCluster:
        print(dictionary, file=file)
print("FATTO2")
print(len(newCluster))
print(newCluster)


#crea file per il pozzo
with open('ground_truth.csv/pozzo6.txt', 'w') as file:
    for dictionary in pozzo:
        print(dictionary, file=file)
print("FATTO3")
print(len(pozzo))
print(pozzo)