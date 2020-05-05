import pandas as pd
from fuzzywuzzy import fuzz

#IN QUESTA NUOVA VERSIONE IL CLUSTER DEI PRODOTTI VIENE TRASFORMATO IN UN DIZIONARIO IN MODO DA LAVORARE SULLE CHIAVI
# IN QUESTA VERSIONE SI LAVORA CON LE CHIAVI DEL DIZIONARIO E SI PRESENTANO TRE CASISTICHE:
#1. SE LE CHIAVI SONO UGUALI UNISCO I CLUSTER
#2. SE UNA CHIAVE E' CONTENUTA NELL'ALTRO CLUSTER —> CONTROLLO GLI ATTRIBUTE VALUE
#3. SE NON C'E' LA CHIAVE FACCIO QUELLO CHE FACEVO PRIMA —> Fai quello che facevi in ground_truth_manager2

def checkSimilarity(attribute_value, lista):
    # CONTROLLARE ADESSO CON LE NUOVE MODIFICHE CHE TIPO SI RICEVE E MODIFICARE LA FUNZIONE
    for value in lista:
        limit = 65
        if len(attribute_value.split()) == 1 or len(attribute_value) < 8 and len(str(value).split()) == 1:
            limit = 84
        ratio = fuzz.ratio(str(attribute_value).lower(), str(value).lower())
        if ratio > limit:
            return True
    return False


newCluster = [] #Nuovo cluster da costruire e riempire. E' un lista di tuple
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterraggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("test_files/product_cluster_for_ground_truth", "r") as file:
    cluster = eval(file.readline())
df = pd.read_csv("ground_truth/ground_truth_random_reducedx2.csv")

# Scorro solo le coppie match
for index, row in df.iterrows():
   target_attribute = row['left_target_attribute']
   # Filtraggio della ground truth prima dell'esecuzione dell'algoritmo
   # Si prendono tutte le righe con lo stesso target attribute. Si scartano tutti quelli che hanno left_attribute e right_attribute
   # 1 SI SCORRE TUTTA LA GROUND TRUTH E SI CREANO DEI CLUSTER CON I SOLI ELEMENTI CHE LA COMPONGONO
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

productCluster = []
# TRASFORMO IL CLUSTER DEI PRODOTTI IN UN DIZIONARIO
# Sono stati creati dei cluster con la ground_truth. Adesso possiamo unire questi cluster con quelli creati nella fase precedente
for product in cluster:
    # product è una lista di tuple con gli attributi del prodotto
    for tupla in product:
        # trasformo gli oggetti in tupla in set così da velocizzare le operazioni successive
        for t in tupla[1]:
            names = set([t[0]])
            values = set([t[1]])
            filename = set([t[2]])
        productCluster.append({tupla[0].replace(" ", "_"): (names,values,filename)})
# CONTROLLARE SE I SET SONO CREATI CORRETTAMENTE
print("FATTO")
print(len(newCluster))



#ADESSO SI PROCEDE AL CONFRONTO FRA DIZIONARI: IL DIZIONARIO DELLA GROUND TRUTH E QUELLO DEI PRODOTTI
for d1 in productCluster:
    #SCORRO TUTTO IL CLUSTER DEI PRODOTTI
    for key1, value1 in d1.items():
        for d2 in newCluster:
            for key2, value2 in d2.items():
            # CASO 1: Esiste già nel cluster della ground truth la chiave. Unisco subito i cluster
                if key1 == key2:
                    for tupla in value1:
                        attribute_name = value1[0].union(value2[0])
                        attribute_value = value1[1].union(value2[1])
                        filename = value1[2].union(value2[2])
                    d2[key2] = (attribute_name,attribute_value,filename)
                    break
                # CASO 2: La chiave è contenuta nella chiave es (Battery è contenuta in battery type)
                elif key1 in key2:
                    attribute_set = value1[0]
                    for attribute in attribute_set:
                        if checkSimilarity(attribute,value2[1]):
                            # unisci cluster
                            for tupla in value1:
                                attribute_name = value1[0].union(value2[0])
                                attribute_value = value1[1].union(value2[1])
                                filename = value1[2].union(value2[2])
                            d2[key2] = (attribute_name, attribute_value, filename)
                            break
                else:
                    #CASO 3: Cerco tra i valori del dizionario
                    attribute_set = value1[0]
                    for attribute in attribute_set:
                        if checkSimilarity(attribute, value2[1]):
                            # unisci cluster
                            for tupla in value1:
                                attribute_name = value1[0].union(value2[0])
                                attribute_value = value1[1].union(value2[1])
                                filename = value1[2].union(value2[2])
                            d2[key2] = (attribute_name, attribute_value, filename)
                            break
            else:
                continue
            break
        # CASO 4 NON HO TROVATO CIO' CHE VERCATO
        newCluster.append({key1: (value1[0], value1[1], value1[2])})


#crea file di output
with open('ground_truth/output3.txt', 'w') as file:
    for dictionary in newCluster:
        print(dictionary, file=file)
print("FATTO2")
print(len(newCluster))
print(newCluster)
