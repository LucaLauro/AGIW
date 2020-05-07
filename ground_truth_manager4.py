import pandas as pd
from fuzzywuzzy import fuzz
from ottimizzazioneClusterName import ottimizzazioneGroundTruh
from nltk.corpus import wordnet

# 1: NON SI CREANO DEI NUOVI CLUSTER - SI USANO SOLO I CLUSTER GIA' CREATI DELLA GROUND TRUTH
# 2: GLI ATTRIBUTI CHE NON VENGONO ACCOPPIATI VENGONO BUTTATI IN UN NUOVO CLUSTER


# Viene in questa versione utilizzato sia per gli attribute name che per gli attribute value
def checkSimilarity(attribute_value, lista):
    for value in lista:
        limit = 65
        if len(attribute_value.split()) == 1 or len(attribute_value) < 8 and len(str(value).split()) == 1:
            limit = 84
        ratio = fuzz.ratio(str(attribute_value).lower(), str(value).lower())
        if ratio > limit:
            return True
    return False

def checkAttributeName(attribute_name, key):
    #Creo prima la lista dei sinonimi dell'attribute_name
        synonyms = []
        for syn in wordnet.synsets(attribute_name):
            for lm in syn.lemmas():
                synonyms.append(lm.name())
        print(set(synonyms))
        # Verifico ora se la chiave è un sinonimo.
        if key in synonyms:
            return True
        return False




newCluster = [] #Nuovo cluster
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterraggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("miniClusterPassata4.txt", "r") as file:
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
            # CASO 1: Esiste già nel cluster della ground truth la chiave. Unisco subito i cluster
                if key1 == key2:
                    for tupla in value1:
                        attribute_name = value1[1].union(value2[0])
                        attribute_value = value1[2].union(value2[1])
                        filename = value1[3].union(value2[2])
                    d2[key2] = (attribute_name,attribute_value,filename)
                    findOne = True
                    break
                # CASO 2: La chiave è contenuta nella chiave es (Battery è contenuta in battery type)
                elif key1 in key2:
                    most_comment_values = value1[0]
                    common_name = most_comment_values[1]
                    if checkSimilarity(common_name,value2[1]):
                        # unisci cluster
                        for tupla in value1:
                            attribute_name = value1[1].union(value2[0])
                            attribute_value = value1[2].union(value2[1])
                            filename = value1[3].union(value2[2])
                        d2[key2] = (attribute_name, attribute_value, filename)
                        findOne = True
                        break

                else:
                    #CASO 3: Faccio il controllo sull'attribute name ma non basta. Controllo anche l'attributevalue
                    # Lavoro con i sinonimi
                    if checkAttributeName(key1,key2):
                        if checkSimilarity(common_name, value2[1]):
                            # unisci cluster
                            for tupla in value1:
                                attribute_name = value1[1].union(value2[0])
                                attribute_value = value1[2].union(value2[1])
                                filename = value1[3].union(value2[2])
                            findOne = True
                            d2[key2] = (attribute_name, attribute_value, filename)
                            break
            else:
                continue
            break
        # CASO 4 NON HO TROVATO CIO' CHE VERCATO
        if not findOne:
            pozzo.append({key1: (value1[1], value1[2], value1[3])})


#crea file di output
with open('ground_truth/final_output4.txt', 'w') as file:
    for dictionary in newCluster:
        print(dictionary, file=file)
print("FATTO2")
print(len(newCluster))
print(newCluster)


#crea file per il pozzo
with open('ground_truth/pozzo4.txt', 'w') as file:
    for dictionary in pozzo:
        print(dictionary, file=file)
print("FATTO3")
print(len(pozzo))
print(pozzo)