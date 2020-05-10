import pandas as pd
from fuzzywuzzy import fuzz
from ottimizzazioneClusterName import ottimizzazioneGroundTruh

def checkSimilarity(attribute_value, lista):
    for value in lista:
        limit = 65
        if len(attribute_value.split()) == 1 or len(attribute_value) < 8 and len(str(value).split()) == 1:
            limit = 84
        ratio = fuzz.ratio(str(attribute_value).lower(), str(value).lower())
        if ratio > limit:
            return True
    return False

# 1: NON SI CREANO DEI NUOVI CLUSTER - SI USANO SOLO I CLUSTER GIA' CREATI DELLA GROUND TRUTH
# 2: GLI ATTRIBUTI CHE NON VENGONO ACCOPPIATI VENGONO BUTTATI IN UN NUOVO CLUSTER


newCluster = []
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterRaggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("miniClusterOttimizzato.txt", "r") as file:
    cluster = eval(file.readline())
df = pd.read_csv("battery_test/ground_truth.csv")

# 1 SI SCORRE TUTTA LA GROUND TRUTH E SI CREANO DEI CLUSTER CON I SOLI ELEMENTI CHE LA COMPONGONO
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

# PRIMA PASSATA: valuto solo le chiavi uguali o uguali parzialmente
for d1 in productCluster:
    for key1, value1 in d1.items():
        listaPossibilita=[]
        for d2 in newCluster:
            for key2, value2 in d2.items():
                str1=str(key1)
                str2=str(key2)
                data = str1.split('_')
                data=list(filter(lambda x : len(str(x))>2, data))
                strClear=str2.replace(' ','_')

                # CASO 1 si deve introdurre una soglia. In listaPossibilita i vincoli devono essere più stringenti
                if str1 == str2 or str1 in str2 or str2 in str1:
                    # Si reintroduce il checkSimilarity?? che succede?
                    if fuzz.token_set_ratio(str1, str2) > 80 or checkSimilarity(value1[0][1],value2[1]):
                        listaPossibilita.append(newCluster.index(d2))
                elif any(parola in strClear for parola in data):
                    if fuzz.token_set_ratio(str1, str2) > 80 or checkSimilarity(value1[0][1],value2[1]):
                        listaPossibilita.append(newCluster.index(d2))
        if len(str(key1)) == 1:  #SI SCARTANO GLI ATTRIBUTI CON UNA SOLA LETTERA
            listaPossibilita=[]

        #CASO 1 e CASO 2: stessa chiave o chiave contenuta
        if len(listaPossibilita) > 0: #stessa cosa di sopra, devo introdurre una soglia
          #  print(listaPossibilita)
          #  print(productCluster.index(d1))
          #  print(key1)

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
                    if len(str(valueAttribute))>4 and len(str(valueAttribute).split(' '))<3:
                        j=j*3
                    maxValue=max(maxValue, j)
                    #print(str(value1[0][1]),'----', str(valueAttribute))
                media=maxName*2+maxValue*3
                tuplePunteggi.append((index,media))

            tuplaMax={"key2":0 }
            #print(tuplePunteggi)
            for tupla in tuplePunteggi:
                if tupla[1]>list(tuplaMax.values())[0]:
                    tuplaMax={tupla[0]:tupla[1]}
            #print(tuplaMax)


            #da controllare questa parte, sicuramente ho fatto casino con gli indici, devo usare gli indici e non d2 sennò sovrascrivo sempre
            #e non accumulo mai
            value2=list(newCluster[list(tuplaMax.keys())[0]].values())[0]
            attribute_name = value1[1].union(value2[0])
            attribute_value = value1[2].union(value2[1])
            filename = value1[3].union(value2[2])
            #print(filename)
            #print(d2[key2])

            #KEY2 DA DOVE SI PRENDE???
            dizionarioDaModificare = newCluster[list(tuplaMax.keys())[0]]
            listaChiavi = list(dizionarioDaModificare.keys())
            chiave = listaChiavi[0]
            newCluster[list(tuplaMax.keys())[0]][chiave] = (attribute_name, attribute_value, filename)
            # print(newCluster[list(tuplaMax.keys())[0]])


for elem in newCluster:
    print(elem)

#crea file di output
with open('ground_truth/final_outputB.txt', 'w') as file:
    for dictionary in newCluster:
        print(dictionary, file=file)
print("FATTO2")
print(len(newCluster))
print(newCluster)