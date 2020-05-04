# [[(brand,{brand:48,manufacturer:2}),(model,{mpn:28,model:39}),...]]
from provaClusterDict import prova_cluster
from fuzzywuzzy import fuzz

with open("miniClusterFiltrato.txt", "r") as file:
    miniCluster = eval(file.readline())


def accettabili(val1, val2):
    sim = fuzz.token_sort_ratio(val1, val2)

    sim2=fuzz.token_set_ratio(val1,val2)
    if sim>50 :
        return True
    if sim>35 and sim < 50 and len(val1)>3 and len(val2)>3 and sim2>50:
        return True
    return False
    


def merge_name_product(dict_product, cluster_product):
    bind = []
    for _, dict_name_attribute in dict_product:
        for key1 in dict_name_attribute:
            for _, d in dict_product:
                for key2 in d:
                    if fuzz.token_set_ratio(key1, key2) > 90:
                        bind += [(key1, key2)]  # a1-a5, a4

    i = 0
    length_cluster_product = len(cluster_product)
    while i < length_cluster_product:

        for attribute in cluster_product[i][1]:
            l = 0
            fatto = False
            for l in range(len(bind)):
                j = i + 1
                key1 = bind[l][0]
                key2 = bind[l][1]
                if key1 == attribute[0]:
                    while j < length_cluster_product:
                        for attribute2 in cluster_product[j][1]:
                            if key2 == attribute2[0]:
                                print(key1, " -- ", key2, " -- ", attribute, " -- ", attribute2)
                                fatto = True #forse spostare fatto in un if accettabili: così scansiono tutte le coppie e non mi fermo alla prima tupla uguale ma solo quando trovo una relazione
                                print(accettabili(attribute[1], attribute2[1]))
                                del bind[l]
                                break
                        if fatto:
                            break
                        j += 1
                elif key2 == attribute[0]:
                    while j < length_cluster_product:
                        for attribute2 in cluster_product[j][1]:
                            if key1 == attribute2[0]:
                                print(key1, " -- ", key2, " -- ", attribute, " -- ", attribute2)
                                fatto = True
                                print(accettabili(attribute[1], attribute2[1]))
                                del bind[l]
                                break
                        if fatto:
                            break
                        j += 1
                if fatto:
                    break
                l += 1
            if fatto:
                break

        i += 1


def merge_by_name(dict_products, cluster_products):
    return 0


N = 188
merge_name_product(prova_cluster()[N], miniCluster[N])

#soglia da cambiare
#minimo sort 50, se sort tra 35 e 50 -> se set è maggiore di 70/80 allora va bene (spero non caghi errori) forse anche 50 ma devo fare i controll
# i e togliere parole più corte di 4 caratteri