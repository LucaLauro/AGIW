""" se non si capisce chiedete ad Andrea
Dal semplice dataset a tutti i prodotti nella nostra struttura dati.
Qui si fa quella che nel doc condiviso, nell'ultima parte scritta, chiamo fase 1.
Quelle che poi si useranno saranno solo "dataset_to_list()" e "data_linkage_to_list()" le altre sono solo di supporto"""

import json
import os

""" prende un percorso e restituisce tutti i nomi dei file al suo interno """
def nomes_file_in_directory(path):
    if os.path.isfile(path): #se è un file
        return [path] #condizione di uscita
    else: #se è una directory
        lista_nomi_file = []
        for filename in os.listdir(path): #per ogni file/directory contenuta nel parametro formalesi ricorre
            lista_nomi_file += nomes_file_in_directory(path + "/" + filename) 
        return lista_nomi_file

""" pulisce le stringhe passate da qualunque carattere brutto (o stringa) """
def clean_value(value):
    bad_ch_list = [']','[', '\n', '@'] #aggiungere qui caratteri o stringhe che si vuole eliminare
    new_value = ""
    for bad_ch in bad_ch_list:
        new_value = value.replace(bad_ch, " ")
    return new_value

""" se è una lista la strasforma in stringa """
def value_to_string(value):
    return value if not isinstance(value, list) else "".join(value)

""" prende un percorso e restituisce una lista di specifiche con i loro attributi:
[(nome file, [(nome attributo, valore attributo), ...]), ...] """
def dataset_to_list(path_to_dataset="./data"):
    list_dataset = []
    for filename in nomes_file_in_directory(path_to_dataset): 
        list_of_single_json = []
        with open(filename) as file_json:  #prende il file
            for (key, value) in json.loads(file_json.read()).items(): #lo apre come un json salva ogni attributo
                list_of_single_json += [(clean_value(key).lower(), clean_value(value_to_string(value)).lower() )] #elimina caratteri brutti e tutto minuscolo
        list_dataset += [(filename[7:], list_of_single_json )]
    return list_dataset
           

""" 
        ---- Attenzione ----
questa funzione l'ho scritto pensando che dovessimo anche scrivere su file il data linkage,
ora però penso che la cosa migliore sia non scrivere nulla su file e tenere tutto in memoria, per ora la lascio così """
"""  
parametri: (il nome del file del data linkage, True se si vuole stampare) 
    se chiamata senza il primo parametro prende il file con nome "dirty_entity_resolution_pictureme.csv"
    se chiamata senza il secondo parametro scrive un file con "dirty_entity_resolution_pictureme-out.csv" 
        con l'output
ritorno:
    None se si sta scrivendo su file, una lista di coppie di nomi di file json equivalenti senza doppio slash
nome del file di input 
[(file1,file2), ...]
"""
def data_linkage_to_list(name_input_file = "dirty_entity_resolution_pictureme.csv", write_on_file = False): 
    file_input = open(name_input_file, "r")
    if write_on_file:
        file_output = open("dirty_entity_resolution_pictureme-no_double_slash.csv", "w")
    else:
        list_of_file_couple = []
    for x in file_input:
        if write_on_file:
            file_output.write(x.replace("//", "/"))
        else:
            list_of_file_couple += [x.replace("//", "/")]
    return list_of_file_couple if not write_on_file else None

