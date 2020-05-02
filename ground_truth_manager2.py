import pandas as pd
from fuzzywuzzy import fuzz

#IN QUESTA NUOVA VERSIONE IL CLUSTER DEI PRODOTTI VIENE TRASFORMATO IN UN DIZIONARIO IN MODO DA LAVORARE SULLE CHIAVI
# E VELOCIZZARE IL PROCESSO

def checkSimilarity(attribute_value, lista):
    if isinstance(lista, set):
        for value in lista:
            limit = 50
            if len(attribute_value.split()) == 1 and len(str(value).split()):
                limit = 80
            ratio = fuzz.ratio(str(attribute_value).lower(), str(value).lower())
            if ratio > limit:
                return True
    else:
        ratio = fuzz.ratio(str(attribute_value).lower(), str(lista).lower())
        if ratio > 80:
            return True
    return False


newCluster = [] #Nuovo cluster da costruire e riempire. E' un lista di tuple
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterraggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("miniClusterPassata2.txt", "r") as file:
    cluster = eval(file.readline())

df = pd.read_csv("ground_truth/ground_truth_random_reducedx2.csv")

# Scorro solo le coppie match
for index, row in df.iterrows():
   target_attribute = row['left_target_attribute']
   # Filtraggio della ground truth prima dell'esecuzione dell'algoritmo
   # Si prendono tutte le righe con lo stesso target attribute. Si scartano tutti quelli che hanno left_attribute e right_attribute
   # 1 SI SCORRE TUTTA LA GROUND TRUTH E SI CREANO DEI CLUSTER CON I SOLI ELEMENTI CHE LA COMPONGONO
   # 2 SI UNISCONO I CLUSTER PRECEDENTEMENTE CREATI DI miniclusterRaggruppato.txt
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
        productCluster.append({tupla[0]: tupla[1]})
print("FATTO")
print(len(newCluster))

#ADESSO SI PROCEDE AL CONFRONTO FRA DIZIONARI: IL DIZIONARIO DELLA GROUND TRUTH E QUELLO DEI PRODOTTI
for d1 in productCluster:
    #SCORRO TUTTO IL CLUSTER DEI PRODOTTI
    for key1, value1 in d1.items():
        # value1 è una lista di tuple del tipo (nomeAttributo, valoreAttributo, NomeFile)
        for tupla in value1:
            attribute_to_check = tupla[1]
            ############################################################
            # SCORRO IL CLUSTER DELLA GROUD TRUTH
            for d2 in newCluster:
                findOne = False
                # newCluster è una lista di dizionari. Li scorro e mi servo della lista di attribute values di ogni dizionario
                for key2, value2 in d2.items():
                    attribute_list = value2[1]
                    #CONTROLLO SIMILARITA' DELL'ATTRIBUTO DELLA TUPLA. SE VA BENE LO AGGIUNGO AD UN DIZIONARIO ESISTENTE E
                    # VADO AVANTI CON LA TUPLA
                    if checkSimilarity(attribute_to_check, attribute_list):
                        if isinstance(value2[0], set):
                            if isinstance(tupla[0], set):
                                new_attribute_name = set().union(value2[0],tupla[0])
                            t = value2[0]
                            t.add(tupla[0])
                            new_attribute_name = t
                        else:
                            new_attribute_name = set([value2[0]]).add(tupla[0])
                        if isinstance(value2[1], set):
                            if isinstance(tupla[1], set):
                                new_attribute_value = set().union(value2[1], tupla[1])
                            u = value2[1]
                            u.add(tupla[1])
                            new_attribute_value = u
                        else:
                            new_attribute_value = set([value2[1]]).add(tupla[1])
                        if isinstance(value2[2], set):
                            if isinstance(tupla[2], set):
                                new_filename = set().union(value2[2],tupla[2])
                            v = value2[2]
                            v.add(tupla[2])
                            new_filename = v
                        else:
                            # ci sono dei valori none
                            if value2[2] is None:
                                new_filename = set([tupla[2]])
                            else:
                                new_filename = set(value2[2]).add(tupla[2])
                        for dictionary in newCluster:
                            if key2 in dictionary:
                                dictionary[key2] = (new_attribute_name, new_attribute_value, new_filename)
                                findOne=True
                                break
                        break
            if not findOne:
            # HO EFFETTUATO LO SCORRIMENTO SU TUTTO IL DIZIONARIO E NON HO TROVATO QUELLO CHE CERCAVO. AGGIUNGO
                name_list = tupla[0]
                if isinstance(tupla[0], set) and isinstance(tupla[1], set) and isinstance(tupla[2], set):
                    newCluster.append({name_list: (tupla[0], tupla[1], tupla[2])})
                newCluster.append({name_list : ({tupla[0]}, {tupla[1]}, {tupla[2]})})
print("FATTO2")
print(len(newCluster))
print(newCluster)
