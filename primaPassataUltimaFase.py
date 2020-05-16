import pandas as pd
from numpy import nan
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from ottimizzazioneClusterName import ottimizzazioneGroundTruh
import json


def checkSimilarity(attribute_value, lista):
    for value in lista:
        limit = 65
        if len(attribute_value.split()) == 1 or len(attribute_value) < 8 and len(str(value).split()) == 1:
            limit = 84
        ratio = fuzz.ratio(str(attribute_value).lower(), str(value).lower())
        if ratio > limit:
            return True
    return False

 #Nuovo cluster
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterraggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("ground_truth/pozzo_manager_output.txt", "r") as file:
    newCluster = eval(file.readline())
with open("datiCompletiCompattati.txt", "r") as file:
    productCluster = eval(file.readline())

#productCluster = [productCluster[10682],productCluster[1993]]
#[{brand:((brand,canon),{brand,manufacturer,...},{canon,...},{www.ebay.com/4274/brand,www.ebay.com/93785/brand...})}]


pozzo = [] #Cluster in cui vengono depositati tutti gli attributi che non si riesce ad accoppiare
#prima passata, valuto solo le chiavi uguali o uguali parzialmente

#i = 0
for d1 in productCluster:
    print(productCluster.index(d1))
    #print(i,"/24500")
    #i = i+1
    for key1, value1 in d1.items():
        listaPossibilita=[]
        for d2 in newCluster:
            for key2, value2 in d2.items():
                str1=str(key1)
                str2=str(key2)
                dataPD = str1.split('_')
                dataPD=list(filter(lambda x : len(str(x))>2, dataPD))
                dataPD=set(dataPD)
                dataGT=set(str2.split('_'))

                if str1 == str2 or str1 in str2 or str2 in str1 or len(dataPD.intersection(dataGT))>0:
                    if fuzz.token_set_ratio(str1.replace("_"," "), str2.replace("_"," ")) > 65 and checkSimilarity(value1[0][1], value2[1]):
                        listaPossibilita.append(newCluster.index(d2))

        if len(str(key1))==1:  #mi capitano attributi con solo 1 lettera che fanno un bordello
            listaPossibilita=[]

        # HO PIU' POSSIBILITA' E PRENDO QUELLA CON IL PUNTEGGIO PIU' ALTO
        # listaPossibilita E' UNA LISTA DI INDICI
        if len(listaPossibilita)> 0:
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
                    if len(str(valueAttribute))>6 and len(str(valueAttribute).split(' '))<3:
                        j=j*2
                    maxValue=max(maxValue, j)
                    #print(str(value1[0][1]),'----', str(valueAttribute))
                media=maxName*4+maxValue*2
                tuplePunteggi.append((index,media))

            tuplaMax={"key2":0 }
            #print(tuplePunteggi)
            for tupla in tuplePunteggi:
                if tupla[1]>list(tuplaMax.values())[0]:
                    tuplaMax={tupla[0]:tupla[1]}

            # PARTE NUOVA: CONTROLLO DEGLI ATTRIBUTE NAME CHE STO ANDANDO AD INSERIRE
            # Si controlla se questi attributi sono molto simili nel nome tra di loro. Uso come metro di giudizio la chiave del dizionario
            # process mi permette di creare una lista di tuple e da questa mi posso ricavare i nomi col punteggio più basso
            key2 = list(newCluster[list(tuplaMax.keys())[0]].keys())[0]
            key2r = str(key2).replace("_"," ")
            listOfScores = process.extract(key2r,value1[1])
            for score in listOfScores:
                if score[1] < 85:
                    # Scorro il cluster della ground truth e vedo se ne trovo uno più adatto al seguente attributo. In caso positivo rimuovo
                    # l'attributo da value2
                    findOne = False
                    for d in newCluster:
                        key = list(d.keys())[0]
                        keyr = str(key).replace("_"," ")
                        # Il confronto lo faccio con la chiave del dizionario
                        if fuzz.ratio(keyr,score[0]) > 80:
                            # Rimuovo l'elemento dal cluster e lo sposto in quello nuovo ma prima recupero il valore associato a quell'attributo
                            # Ci sono casi in cui il file non è definito ATTENZIONE
                            if value1[3]:
                                fileList = set()
                                for file in value1[3]:
                                    find = False
                                   # Cerco nella stringa
                                   # Se il nome del file ha come delimitatore /  vedi caso di ebay (www.ebay.com/24539/screen size) bisogna trattarlo diversamente
                                    if len(file.split("//")) == 1: # sono nel caso con un solo /
                                        if file.split("/")[2] == score[0]:
                                            find = True
                                            producer = file.split("/")[0]
                                            product = file.split("/")[1]
                                            fileList.add(file)
                                    elif file.split("//")[2] == score[0] :
                                        find = True
                                        producer = file.split("//")[0]
                                        product = file.split("//")[1]
                                        fileList.add(file)
                                    if find:
                                        path = 'data/' + producer + '/' + product + ".json"  # carico il file del prodotto
                                        f = open(path)
                                        data = json.load(f)
                                        for (k, v) in data.items():
                                            if '(more than' in v:  # elimino i (more than xx%) che danno fastidio
                                                i = v.index('(')
                                                v = v[:i]
                                            if type(v) == list:
                                                v = str(v).strip('[]')
                                            if k == score[0]:
                                                # ho trovato la chiave corrispondente. Controllo il valore. 1 controllo sulle parole
                                                if len(v.split(" ")) < 4:
                                                    for v2 in list(d.values())[0][1]:
                                                        if fuzz.token_sort_ratio(v,v2) > 80:
                                                            if v in value1[2]:
                                                                value1[2].remove(v)
                                                            if score[0] in value1[1]:
                                                                value1[1].remove(score[0])
                                                            # value1[3].remove(file)
                                                            # modifico il cluster aggiungendo il nuovo valore appena recuperato
                                                            value_to_modify = list(d.values())[0]
                                                            attribute_name = value_to_modify[0].union({score[0]})
                                                            attribute_value = value_to_modify[1].union({v})
                                                            filename = value_to_modify[2].union({file})
                                                            newCluster[newCluster.index(d)][key] = (attribute_name, attribute_value, filename)
                                                            findOne = True
                                                            break
                                                        if findOne:
                                                            break
                                                else:

                                                    for v2 in list(d.values())[0][1]:
                                                        if fuzz.token_sort_ratio(v,v2) > 65:
                                                            if v in value1[2]:
                                                                value1[2].remove(v)
                                                            if score[0] in value1[1]:
                                                                value1[1].remove(score[0])
                                                            # value1[3].remove(file)
                                                            # modifico il cluster aggiungendo il nuovo valore appena recuperato
                                                            value_to_modify = list(d.values())[0]
                                                            attribute_name = value_to_modify[0].union({score[0]})
                                                            attribute_value = value_to_modify[1].union({v})
                                                            filename = value_to_modify[2].union({file})
                                                            newCluster[newCluster.index(d)][key] = (attribute_name, attribute_value, filename)
                                                            findOne = True
                                                            break
                                                        if findOne:
                                                            break
                                for el in fileList:
                                    value1[3].remove(el)

                        if not findOne:
                            for name in list(d.values())[0][0]:
                                if fuzz.ratio(name, score[0]) > 80:
                                    # Rimuovo l'elemento dal cluster e lo sposto in quello nuovo ma prima recupero il valore associato a quell'attributo
                                    # Ci sono casi in cui il file non è definito ATTENZIONE
                                    if value1[3]:
                                        fileList = set()
                                        for file in value1[3]:
                                            find = False
                                            # Cerco nella stringa
                                            # Se il nome del file ha come delimitatore /  vedi caso di ebay (www.ebay.com/24539/screen size) bisogna trattarlo diversamente
                                            if len(file.split("//")) == 1:  # sono nel caso con un solo /
                                                if file.split("/")[2] == score[0]:
                                                    find = True
                                                    producer = file.split("/")[0]
                                                    product = file.split("/")[1]
                                                    fileList.add(file)
                                            elif file.split("//")[2] == score[0]:
                                                find = True
                                                producer = file.split("//")[0]
                                                product = file.split("//")[1]
                                                fileList.add(file)
                                            if find:
                                                path = 'data/' + producer + '/' + product + ".json"  # carico il file del prodotto
                                                f = open(path)
                                                data = json.load(f)
                                                for (k, v) in data.items():
                                                    if '(more than' in v:  # elimino i (more than xx%) che danno fastidio
                                                        i = v.index('(')
                                                        v = v[:i]
                                                    if type(v) == list:
                                                        v = str(v).strip('[]')
                                                    if k == score[0]:
                                                        # ho trovato la chiave corrispondente. Controllo il valore. 1 controllo sulle parole
                                                        if len(v.split(" ")) < 4:
                                                            for v2 in list(d.values())[0][1]:
                                                                v2 = str(v2)
                                                                if fuzz.token_sort_ratio(v, v2) > 80:
                                                                    if v in value1[2]:
                                                                        value1[2].remove(v)
                                                                    if score[0] in value1[1]:
                                                                        value1[1].remove(score[0])
                                                                    # value1[3].remove(file)
                                                                    # modifico il cluster aggiungendo il nuovo valore appena recuperato
                                                                    value_to_modify = list(d.values())[0]
                                                                    attribute_name = value_to_modify[0].union(
                                                                        {score[0]})
                                                                    attribute_value = value_to_modify[1].union({v})
                                                                    filename = value_to_modify[2].union({file})
                                                                    newCluster[newCluster.index(d)][key] = (
                                                                    attribute_name, attribute_value, filename)
                                                                    findOne = True
                                                                    break
                                                                if findOne:
                                                                    break
                                                        else:
                                                            for v2 in list(d.values())[0][1]:
                                                                if fuzz.token_sort_ratio(v, v2) > 65:
                                                                    if v in value1[2]:
                                                                        value1[2].remove(v)
                                                                    if score[0] in value1[1]:
                                                                        value1[1].remove(score[0])
                                                                    # value1[3].remove(file)
                                                                    # modifico il cluster aggiungendo il nuovo valore appena recuperato
                                                                    value_to_modify = list(d.values())[0]
                                                                    attribute_name = value_to_modify[0].union(
                                                                        {score[0]})
                                                                    attribute_value = value_to_modify[1].union({v})
                                                                    filename = value_to_modify[2].union({file})
                                                                    newCluster[newCluster.index(d)][key] = (
                                                                    attribute_name, attribute_value, filename)
                                                                    findOne = True
                                                                    break
                                                                if findOne:
                                                                    break
                                        for el in fileList:
                                            value1[3].remove(el)

            value2 = list(newCluster[list(tuplaMax.keys())[0]].values())[0]
            attribute_name = value1[1].union(value2[0])
            attribute_value = value1[2].union(value2[1])
            filename = value1[3].union(value2[2])
            #print(filename)
            #print(d2[key2])
            newCluster[list(tuplaMax.keys())[0]][key2] = (attribute_name, attribute_value, filename)
            #print(newCluster[list(tuplaMax.keys())[0]])

        if not listaPossibilita :
            pozzo.append({key1: (value1[0], value1[1], value1[2], value1[3])})


#crea file di output
with open('out_ultima_fase/ultimaPassataOut.txt.txt', 'w') as file:
    file.write(str(newCluster))
print("FATTO2")



#crea file per il pozzo
with open("out_ultima_fase/ultimaPassataPozzo.txt.txt", "w") as file:
    file.write(str(pozzo))
print("FATTO3")
print(len(pozzo))
print(pozzo)