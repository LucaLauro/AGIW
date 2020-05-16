import pandas as pd

f = "ground_truth/instance_attributes_gt.csv"
data = pd.read_csv(f)
dati = data[data['label'] == 1]

cluster_ground_truth = []

for index, row in data.iterrows():
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
   if any(target_attribute in d for d in cluster_ground_truth):
       for dictionary in cluster_ground_truth:
           if target_attribute in dictionary.keys():
               valori = list(dictionary.values())[0]
               newAttributeNameList = set().union(valori[0], attributeNameList)
               newAttributeValueList = set().union(valori[1], attributeValueList)
               newfileNameList = set().union(valori[2], fileNameList)
               dictionary[target_attribute] = (newAttributeNameList, newAttributeValueList, newfileNameList)
   else:
       cluster_ground_truth.append({target_attribute: (attributeNameList, attributeValueList, fileNameList)})

#Si recupera il file di output
#output_cluster = []
#with open("out_finale.txt", "r") as file:
#    output_cluster = eval(file.readline())

#PRECISION: Si verifica se i cluster della ground truth sono rispettati
#Il controllo verrà fatto tramite il filename