from fuzzywuzzy import fuzz
from numpy import nan

with open("ground_truth/pozzo8.txt", "r") as file:
    pozzo = eval(file.readline())

with open("ground_truth/manager8_output.txt", "r") as file:
    cluster = eval(file.readline())

pozzo2 = []

for line in pozzo:
    for key, value in line.items():
        listaPossibilita = []
        for row in cluster:
            for key2,value2 in row.items():
                for attribute_name in value2[1]:
                    if fuzz.token_set_ratio(value[0][0], attribute_name) > 75:
                        listaPossibilita.append(cluster.index(row))
                        break
        if len(listaPossibilita) > 0:
            tuplePunteggi=[]
            for index in listaPossibilita:
                value2 = list(cluster[index].values())[0]
                maxName = 0
                for nameAttribute in value2[0]:
                    i = fuzz.token_set_ratio(str(value[0][0]), str(nameAttribute))
                    maxName= max(maxName,i)
                    #print(str(value1[0][0]),'----',str(nameAttribute))
                maxValue = 0
                for valueAttribute in value2[1]:
                    j = fuzz.token_set_ratio(str(value[0][1]), str(valueAttribute))
                    if len(str(valueAttribute))>6 and len(str(valueAttribute).split(' '))<3:
                        j=j*2
                    maxValue=max(maxValue, j)
                    #print(str(value1[0][1]),'----', str(valueAttribute))
                media=maxName*4+maxValue*2
                tuplePunteggi.append((index,media))

            tuplaMax={"key2": 0 }
            #print(tuplePunteggi)
            for tupla in tuplePunteggi:
                if tupla[1]>list(tuplaMax.values())[0]:
                    tuplaMax={tupla[0]:tupla[1]}

            value2 = list(cluster[list(tuplaMax.keys())[0]].values())[0]
            attribute_name = value[1].union(value2[0])
            attribute_value = value[2].union(value2[1])
            filename = value[3].union(value2[2])
            cluster[list(tuplaMax.keys())[0]][key2] = (attribute_name, attribute_value, filename)

        if not listaPossibilita:
            pozzo2.append({key: (value[0], value[1], value[2], value[3])})

#crea file di output
with open('ground_truth/pozzo_manager_output.txt', 'w') as file:
    for dictionary in cluster:
        print(dictionary, file=file)
print("FATTO")



#crea file per il pozzo
with open('ground_truth/pozzo_manager_pozzo.txt', 'w') as file:
    for dictionary in pozzo2:
        print(dictionary, file=file)
print("FATTO2")
print(len(pozzo2))
print(pozzo2)