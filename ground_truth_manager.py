import pandas as pd
from py_thesaurus import Thesaurus

newCluster = [] #Nuovo cluster da costruire e riempire. E' un lista di tuple
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterraggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("miniClusterRaggruppato.txt", "r") as file:
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
               newfileNameList = valori[2] + fileNameList
               dictionary[target_attribute] = (newAttributeNameList, newAttributeValueList, newfileNameList)
   else:
       newCluster.append({target_attribute: (attributeNameList, attributeValueList, fileNameList)})

# Sono stati creati dei cluster con la ground_truth. Adesso possiamo unire questi cluster con quelli creati nella fase precedente
for product in cluster:
    # product è una lista di tuple con gli attributi del prodotto
    for attributes in product: #Salto la posizione zero che è solo il nome del cluster
        attribute = attributes[1] # tupla con gli attributi
        for tupla in attribute:
            print('ciao')




#def sameCluster(target_attribute,left_attribute,right_attribute,*tupla):
#    ldata = left_attribute.split("/")
#    lattribute = ldata[2]
#    rdata = right_attribute.split("/")
#    rattribute = rdata[2]
 #   if target_attribute == tupla[0] or synonimous(target_attribute, tupla[0]):
#       #TODO: Da finire da implementare
 #       return True



#def synonimous(attribute_name, target_atribute):
#    target_synonims = Thesaurus(target_attribute)
#    synonims = (target_synonims.get_synonym())
#    if attribute_name in synonims:
#        return True
#    else #Si cerca nel dizionario dei sinonimi
#    #TODO: Da implementare il dizionario di sinonimi
#    return True