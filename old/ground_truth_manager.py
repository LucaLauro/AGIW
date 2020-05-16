import pandas as pd
from fuzzywuzzy import fuzz


def checkSimilarity(lista, attribute_value):
    for value in lista:
        limit = 50
        if len(attribute_value.split()) == 1:
            limit = 80
        ratio = fuzz.ratio(str(attribute_value).lower(), str(value).lower())
        if ratio > limit:
            # 'Canon' e 'none' possono finire insieme (ratio 67)
            print(attribute_value + "NNNNNN" + value + "NNNNNNN" + str(ratio) + " NON FORMA UN NUOVO CLUSTER\n")
            return True
    print(attribute_value + "NNNNN" + value + "NNNNNN"+  str(ratio) + " FORMA UN NUOVO CLUSTER\n")
    return False


newCluster = [] #Nuovo cluster da costruire e riempire. E' un lista di tuple
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterraggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("miniClusterPassata2.txt", "r") as file:
    cluster = eval(file.readline())

df = pd.read_csv("ground_truth.csv/ground_truth_random_reducedx2.csv")

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

# Sono stati creati dei cluster con la ground_truth.csv. Adesso possiamo unire questi cluster con quelli creati nella fase precedente
for product in cluster:
    # product è una lista di tuple con gli attributi del prodotto
    for tupla in product:
         #Salto la posizione zero che è solo il nome del cluster
         # Lo 0 è il nome del cluster e viene saltato
         clusterItemsList = tupla[1] #Ho una lista di tuple ('nome attributo', 'valore attributo', 'nome file')
         for item in clusterItemsList: #item è la tupla ('nome attributo', 'valore attributo', 'nome file')
             attributeValue = item[1] # faccio il check solo sul valore
             #Scorro adesso il cluster e vedo se ci sono valori simili con cui può essere accoppiato
             for dictionary in newCluster:
                 # alist è una lista di tuple
                 alist= list(dictionary.values())[0] #i valori di un dizionario non sono iterabili e quindi si fa questo passaggio aggiuntivo
                 attributeListCluster = list(alist[1]) #è la lista di attributi nel cluster
                 if checkSimilarity(attributeListCluster, attributeValue):
                     nameClusterList = alist[0].union([item[0]])
                     valueClusterList = set(attributeListCluster).union([item[1]])
                     fileClusterList = set([item[2]]).union(alist[2])
                     keyDictionary = list(dictionary.keys())[0]
                     dictionary[keyDictionary] = (nameClusterList, valueClusterList, fileNameList)
                     break
         nameClusterList = set([item[0]]) # prima la conversione in lista perchè il set di una stringa mi restituisce un set di caratteri
         valueClusterList = set([item[1]])
         fileClusterList = set([item[2]])
         clusterName = [item[0]][0]
         newCluster.append({clusterName: (nameClusterList,valueClusterList,fileClusterList)})
print("FATTO")
