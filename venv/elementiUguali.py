import json
import pandas as pd

df = pd.read_csv('/Users/luca/PycharmProjects/agiw/venv/dirty_entity_resolution_pictureme.csv')
dict = {}
valoriUsati=[]
for index, row in df.iterrows():
    if row['left_spec_id'] in dict and row['right_spec_id']  not in valoriUsati:
        dict[row['left_spec_id']].append(row['right_spec_id'])
        valoriUsati.append(row['right_spec_id'])
    elif row['right_spec_id']  not in valoriUsati and row['left_spec_id']  not in valoriUsati:
        dict.update({row['left_spec_id'] : [row['right_spec_id']]})
        valoriUsati.append(row['right_spec_id'])
        valoriUsati.append(row['left_spec_id'])

#fare metodo per liste XD



with open('/Users/luca/PycharmProjects/agiw/venv/MyFile.txt', 'w+') as file:
     file.write(json.dumps(dict))

#metodo per prendere tutti quelli uguali dato un id
"""

def trovaUguali(dict):
    for index, row in df[df['left_spec_id'] == idProva].iterrows():
        if not row['right_spec_id'] in idUguali:
            dict.append(row['right_spec_id'])
    for index, row in df[df['right_spec_id'] == idProva].iterrows():
        if not row['left_spec_id'] in idUguali:
            dict.append(row['left_spec_id'])

    print(dict)"""