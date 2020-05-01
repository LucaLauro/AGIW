with open("raggruppato.txt", "r") as file:
    lista = eval(file.readline())



def group_cluster_in_products(list_binding):
    group_binding = []
    for product, b1, b2 in list_binding:
        while len(group_binding)-1<product:
            group_binding += [[]]
        if len(group_binding)>product:
            non_messo = True
            for i in range(len(group_binding[product])):
                if b1 in group_binding[product][i]:
                    if not b2 in group_binding[product][i]:
                        group_binding[product][i] += [b2]
                    non_messo=False
                else:
                    if b2 in group_binding[product][i]:
                        if not b1 in group_binding[product][i]:
                            group_binding[product][i] += [b1]  
                        non_messo=False
            if non_messo:
                group_binding[product] += [[b1]+[b2]]
        else:
            group_binding += [[[b1]+[b2]]]
    return group_binding
  
print(group_cluster_in_products(lista))
