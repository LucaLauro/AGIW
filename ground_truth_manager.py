import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from py_thesaurus import Thesaurus

def checkSimilarity(dictionary, attribute_value, attribute_name):
    check_similarity = False
    dictionary = list(dictionary.values())[0]
    for value in dictionary[1]:
        if fuzz.ratio(str(attribute_value).lower(), str(value).lower()) > 60:
            # 'Canon' e 'none' possono finire insieme (ratio 67)
            check_similarity = True
    return check_similarity

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

# Sono stati creati dei cluster con la ground_truth. Adesso possiamo unire questi cluster con quelli creati nella fase precedente
for product in cluster:
    # product è una lista di tuple con gli attributi del prodotto
    for attributes in product: #Salto la posizione zero che è solo il nome del cluster
        attribute = attributes[1] # tupla con gli attributi
        for tupla in attribute:
            findOne = False #Booleano che controlla se è già presente un cluster che può accogliere l'attributo. Se è false si crea un nuovo cluster
            # Scorro dentro i cluster, prima cerco tra gli attribute name e poi negli attribute value
            for dictionary in newCluster:
                if checkSimilarity(dictionary,tupla[1],tupla[0]):
                    newValori = list(dictionary.values())[0]
                    valueList = set().union(newValori[1],[tupla[1]])
                    nameList = set().union(newValori[0], [tupla[0]])
                    fileList = set().union(newValori[2], [tupla[2]])
                    key = list(dictionary.keys())[0]
                    dictionary[key] = (nameList, valueList, fileList)
                    findOne = True
            if findOne is False:
                valueList = set([tupla[1]])
                nameList = set([tupla[0]])
                fileList = set([tupla[2]])
                newCluster.append({tupla[0] : (nameList,valueList,fileList)})

print("FATTO")

with open('ground_truth_output', 'w') as f:
    #Trasformo i dizionari in una lista per la fase successiva
    for d in newCluster:
        fromDictionaryToList = [(k, v) for k, v in d.items()]
        for item in fromDictionaryToList:
            f.write("%s\n" % item)
