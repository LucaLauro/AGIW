import pandas as pd
from fuzzywuzzy import fuzz
import json

#IN QUESTA NUOVA VERSIONE IL CLUSTER DEI PRODOTTI VIENE TRASFORMATO IN UN DIZIONARIO IN MODO DA LAVORARE SULLE CHIAVI
# E VELOCIZZARE IL PROCESSO

def checkSimilarity(attribute_value, lista):
    if isinstance(lista, set):
        for value in lista:
            limit = 60
            if len(attribute_value.split()) == 1 and len(str(value).split()):
                limit = 84
            ratio = fuzz.ratio(str(attribute_value).lower(), str(value).lower())
            if ratio > limit:
                return True
    else:
        limit = 60
        if len(attribute_value.split()) == 1 and len(str(lista).split()):
            limit = 84
        ratio = fuzz.ratio(str(attribute_value).lower(), str(lista).lower())
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
       # crea file di output
   with open('ground_truth/ground_truth_cluster.txt', 'w') as file:
       for dictionary in newCluster:
           print(dictionary, file=file)


productCluster = []
# TRASFORMO IL CLUSTER DEI PRODOTTI IN UN DIZIONARIO
# Sono stati creati dei cluster con la ground_truth. Adesso possiamo unire questi cluster con quelli creati nella fase precedente
for product in cluster:
    # product è una lista di tuple con gli attributi del prodotto
    for tupla in product:
        productCluster.append({tupla[0]: tupla[1]})
print("FATTO")
print(len(newCluster))
#crea file di output
with open('ground_truth/product_cluster.txt', 'w') as file:
    for dictionary in productCluster:
        print(dictionary, file=file)

#ADESSO SI PROCEDE AL CONFRONTO FRA DIZIONARI: IL DIZIONARIO DELLA GROUND TRUTH E QUELLO DEI PRODOTTI
for d1 in productCluster:
    #SCORRO TUTTO IL CLUSTER DEI PRODOTTI
    for key1, value1 in d1.items():
        # value1 è una lista di tuple del tipo (nomeAttributo, valoreAttributo, NomeFile)
        # il controllo viene fatto sulla prima tupla. Se va a buon fine allora viene aggiunto al cluster
        tupla= value1[0]
        attribute_to_check = tupla[1]
        ############################################################
        # SCORRO IL CLUSTER DELLA GROUD TRUTH
        for d2 in newCluster:
            # newCluster è una lista di dizionari. Li scorro e mi servo della lista di attribute values di ogni dizionario
            for key2, value2 in d2.items():
                findOne = False
                attribute_list = value2[1]
                #CONTROLLO SIMILARITA' DELL'ATTRIBUTO DELLA TUPLA. SE VA BENE LO AGGIUNGO AD UN DIZIONARIO ESISTENTE E
                # VADO AVANTI CON LA TUPLA
                if checkSimilarity(attribute_to_check, attribute_list):
                    # mi creo il nuovo set di tuple
                    attribute_name = set()
                    attribute_value = set()
                    filename = set()
                    #IL CHECK VA A BUON FINE E AGGIUNGO NON SOLO QUELLA TUPLA MA TUTTE LE TUPLE NEL DIZIONARIO
                    for t in value1:
                        if isinstance(t[0], str):
                            attribute_name.add(t[0])
                        else:
                            attribute_name.union(t[0])
                        if isinstance(t[1], str):
                            attribute_value.add(t[1])
                        else:
                            attribute_value.union(t[1])
                        if isinstance(t[2], str):
                            filename.add(t[2])
                        else:
                           filename.union(t[2])
                    new_attribute_name = attribute_name.union(value2[0])
                    new_attribute_value = attribute_value.union(value2[1])
                    new_filename = filename.union(value2[2])
                    # poi fondo con i valori del cluster
                    for dictionary in newCluster:
                        if key2 in dictionary:
                            dictionary[key2] = (new_attribute_name, new_attribute_value, new_filename)
                            findOne = True
                            break
                    #HO TROVATO UN DIZIONARIO CHE PUO' ACCOGLIERE LA MIA TUPLA. ESCO DAL CICLO
                    break
        if not findOne:
            attribute_name = set()
            attribute_value = set()
            filename = set()
            for t in value1:
                # HO EFFETTUATO LO SCORRIMENTO SU TUTTO IL DIZIONARIO E NON HO TROVATO QUELLO CHE CERCAVO. AGGIUNGO
                # creo la lista degli attribute name
                # creo la lista degli attribute value
                attribute_name.add(t[0])
                attribute_value.add(t[1])
                filename.add(t[2])
            newCluster.append({key1: (attribute_name, attribute_value, filename)})
print("FATTO2")
print(len(newCluster))
print(newCluster)

#crea file di output
with open('ground_truth/output.txt', 'w') as file:
    for dictionary in newCluster:
        print(dictionary, file=file)
