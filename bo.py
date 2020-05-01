# prendo in input una lista di tuple del tipo [(0,2,4),(0,4,6),...] dove il primo elemento specifica il numero del prodotto
# il secondo numero dellla tupla il cluster principale in cui va raggruppato il terzo elemento della tupla
# l'out della funzione è una lista di liste dove ogni lista contiene tutti gli indici degli elementi che vanno raggruppati insieme
with open("raggruppato.txt", "r") as file:
    lista = eval(file.readline())


def group_cluster_in_products(list_binding):
    group_binding = []
    for product, b1, b2 in list_binding:
        while len(group_binding) - 1 < product:
            group_binding += [[]]
        if len(group_binding) > product:
            lista_appoggio = [b1, b2]
            for i in range(len(group_binding[product])):
                if (b1 in group_binding[product][i]) or (b2 in group_binding[product][i]):
                    lista_appoggio += group_binding[product][i]
                    group_binding[product][i] = [0]
            group_binding[product] += [list(set(lista_appoggio))]

        else:
            group_binding += [[[b1] + [b2]]]
    for lista_prodotti in range(len(group_binding)):
        group_binding[lista_prodotti] = list(filter(lambda x: x != [0], group_binding[lista_prodotti]))
    return group_binding

with open("raggruppatoDaAndrea.txt", "w") as file:
    file.write(str(group_cluster_in_products(lista)))

