import pandas as pd

newCluster = [] #Nuovo cluster da costruire e riempire
cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
# Ogni lista in miniclusterraggruppato rappresenta un prodotto. All'interno di quel prodotto ha una lista di tuple che
# rappresentano gli attributi di quel prodotto
with open("miniClusterRaggruppato.txt", "r") as file:
    cluster = eval(file.readline())

# Leggi la ground truth in un Pandas dataframe
df = pd.read_csv('ground_truth/instance_attributes_gt.csv')

# Scorro solo le coppie match
for index, row in df[df['label'] == 1].iterrows():
   target_attribute = row['left_target_attribute']
   left_attribute = row['left_instance_attribute']
   right_attribute = row['right_instance_attribute']
   for product in cluster:
       # product è una lista di tuple con gli attributi del prodotto
       for attributes in product: #Salto la posizione zero che è solo il nome del cluster
            attribute = attributes[1] # tupla con gli attributi
            for tupla in attribute:
                if sameCluster(target_attribute,left_attribute,right_attribute,tupla):
                    #Aggiungo al nuovo cluster
           #Quando si vuole aggiungere un nuovo elemento al cluster occorre controllare che non sia già presente



def sameCluster(target_attribute,left_attribute,right_attribute,*tupla):
    ldata = left_attribute.split("/")
    lattribute = ldata[2]
    rdata = right_attribute.split("/")
    rattribute = rdata[2]
    if target_attribute == tupla[0] or synonimous(target_attribute, tupla[0]):
       #TODO: Da finire da implementare
        return True



def synonimous(attribute_name, target_atribute):
    #TODO: Da implementare il dizionario di sinonimi
    return True