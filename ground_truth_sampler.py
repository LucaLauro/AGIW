import random
import pandas as pd


#Questo file è stato creato per generare una ground truth più piccola e velocizzare la fase di sviluppo
#Questa operazione è molto lenta. Il file csv viene salvato tutto in memoria per prendere solo le righe che hanno label=1

# TODO: Trovare un criterio per cui estrarre gli esempi più importanti
# SOLUZIONE TEMPORANEA: Sample random dei dati per velocizzare la computazione
#df = pd.read_csv("ground_truth.csv/instance_attributes_gt.csv")
#dati = df[df['label'] == 1]
#dati.sample(n=5)
#dati.to_csv(r'ground_truth.csv/ground_truth_random_5.csv', index=False, header=True)



#Secondo approccio più veloce
# The data to load
#f = "ground_truth.csv/instance_attributes_gt.csv"
# Considero ogni 20000 righe
#n = 20000
#num_lines = sum(1 for l in open(f))
# Salto l'header
#skip_idx = [x for x in range(1, num_lines) if x % n != 0]
# Leggo i dati e prendo solo quelli con label=1
#data = pd.read_csv(f, skiprows=skip_idx)
#dati = data[data['label'] == 1]
#dati.to_csv(r'ground_truth.csv/ground_truth_random_reducedx2.csv', index=False, header=True)
#print("FATTO")


#Test che prende tutte le colonne e ne elimina i duplicati
#f = "ground_truth.csv/instance_attributes_gt.csv"
#data = pd.read_csv(f)
#dati = data[data['label'] == 1]
#dati = dati.drop_duplicates(subset=['left_target_attribute'], keep='first')
#dati.to_csv(r'ground_truth.csv/test_no_duplicates.csv', index=False, header=True)

# Elimina i duplicati che hanno stesso left_target_attribute e stesso left_instance_value e right_instance_value e gli attributi noisy
#f = "ground_truth.csv/instance_attributes_gt.csv"
#data = pd.read_csv(f)
#dati = data[data['label'] == 1]
#all_battery_chemistry = dati.loc[dati['left_target_attribute'] == 'battery_chemistry']
#dati = dati.drop_duplicates(subset=['left_target_attribute', 'left_instance_value'], keep='first')
#dati = dati.drop_duplicates(subset=['left_target_attribute', 'right_instance_value'], keep='first')
#dati['left_instance_value'] = dati['left_instance_value'].astype('str')
#dati['right_instance_value'] = dati['right_instance_value'].astype('str')
#mask = (dati['left_instance_value'].str.len() < 10) & (dati['right_instance_value'].str.len() < 10)
#dati = dati.loc[mask]
#frames = [dati, all_battery_chemistry]
#result = pd.concat(frames)
#result = result.drop_duplicates(subset=['left_target_attribute', 'left_instance_value'], keep='first')
#result = result.drop_duplicates(subset=['left_target_attribute', 'right_instance_value'], keep='first')
#result.to_csv(r'ground_truth.csv/test_no_duplicates3.csv', index=False, header=True)


#Nuova versione: 100 righe per ogni attributo
f = "ground_truth/instance_attributes_gt.csv"
data = pd.read_csv(f)
dati = data[data['label'] == 1]
dati = dati.groupby("left_target_attribute").head(50)
dati.to_csv(r'ground_truth/test50.csv', index=False, header=True)


