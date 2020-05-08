import pandas as pd
from fuzzywuzzy import fuzz
from ottimizzazioneClusterName import ottimizzazioneGroundTruh


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

newCluster = [] #Nuovo cluster
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterraggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("miniClusterOttimizzato.txt", "r") as file:
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

#prima passata, valuto solo le chiavi uguali o uguali parzialmente


for d1 in productCluster:
    for key1, value1 in d1.items():
        listaPossibilita=[]
        for d2 in newCluster:
            findOne = False
            for key2, value2 in d2.items():

                if str(key1) == str(key2):
                    listaPossibilita=[newCluster.index(d2)]
                    findOne=True
                    break
                elif str(key1) in str(key2):
                    listaPossibilita.append(newCluster.index(d2))
                elif str(key2) in str(key1):
                    listaPossibilita.append(newCluster.index(d2))

            if findOne:
                break
        if len(listaPossibilita)==1:
            value2= list(newCluster[listaPossibilita[0]].values())[0]
            attribute_name = value1[1].union(value2[0])
            attribute_value = value1[2].union(value2[1])
            filename = value1[3].union(value2[2])
            d2[key2] = (attribute_name, attribute_value, filename)

        elif len(listaPossibilita)>1:

            tuplePunteggi=[]
            for key2 in listaPossibilita:
                value2 = list(newCluster[key2].values())[0]
                maxName = 0
                for nameAttribute in value2[0]:
                    i = fuzz.token_set_ratio(value1[0][0], nameAttribute)
                    maxName= max(maxName,i)
                maxValue = 0
                for valueAttribute in value2[1]:
                    j = fuzz.token_set_ratio(value1[0][1], valueAttribute)
                    maxValue=max(maxValue, j)
                media=maxName*5+maxValue*2
                tuplePunteggi.append((key2,media))

            tuplaMax={"key2":0 }
            for tupla in tuplePunteggi:
                if tupla[1]>list(tuplaMax.values())[0]:
                    tuplaMax={tupla[0]:tupla[1]}

            value2=list(newCluster[list(tuplaMax.keys())[0]].values())[0]
            attribute_name = value1[1].union(value2[0])
            attribute_value = value1[2].union(value2[1])
            filename = value1[3].union(value2[2])
            d2[key2] = (attribute_name, attribute_value, filename)



for elem in newCluster:
    print(elem)