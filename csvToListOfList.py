import json
import pandas as pd

df = pd.read_csv('dirty_entity_resolution_pictureme.csv')

csvToListOfList = []
valoriUsati =[]

for index, row in df.iterrows():           # scansiono tutto il csv
    if row['left_spec_id'] in valoriUsati and row['right_spec_id']  not in valoriUsati:  #se è presente il valore left nei valori usati allora per inserire
        for i,list in enumerate(csvToListOfList):                                              #il destro cerco l'indice della l'ista dove è presente e lo inserisco
            if row['left_spec_id'] in list:
                indiceElemento= i
        csvToListOfList[indiceElemento].append(row['right_spec_id'])
        valoriUsati.append(row['right_spec_id'])
    elif row['right_spec_id'] not in valoriUsati and row['left_spec_id'] not in valoriUsati:
        csvToListOfList.append([row['left_spec_id'],row['right_spec_id']])
        valoriUsati.append(row['left_spec_id'])
        valoriUsati.append(row['right_spec_id'])

with open("csvToListOfList.txt", "w") as file:
    file.write(str(csvToListOfList))
#print(type(csvToListOfList), type(csvToListOfList[0]), type(csvToListOfList[0][0]))

