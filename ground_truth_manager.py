import pandas as pd


# Leggi la ground truth in un Pandas dataframe
df = pd.read_csv('ground_truth/instance_attributes_gt.csv')

cluster = []
#Prendo la lista di cluster generata nella fase precedente miniclusterRaggruppato.txt
with open("miniClusterRaggruppato.txt", "r") as file:
    cluster = eval(file.readline())

# Stampa le prime 5 righe del dataframe
print(df.head())

# Scorri l’intero dataframe (N.B. operazione lenta)
#for index, row in df.iterrows():
 #   left_attribute = row['left_instance_attribute']
 #   right_attribute = row['right_instance_attribute']
 #   print(left_attribute, right_attribute)

# Scorro solo le coppie match
#for index, row in df[df['label'] == 1].iterrows():
#    target_attribute = row['left_target_attribute']
#    # if cluster.co
#    left_attribute = row['left_instance_attribute']
#    right_attribute = row['right_instance_attribute']

 #   print(left_attribute, right_attribute)

