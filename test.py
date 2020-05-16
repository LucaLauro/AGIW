from fuzzywuzzy import fuzz

with open("out_ultima_fase/ultimaPassataPozzo.txt", "r") as file:
    cluster = eval(file.readline())
clusterCompatto=[]

print(len(cluster))
for indexElem in range(len(cluster)):
    scritto=False
    print(indexElem)
    print(len(clusterCompatto))
    for indexCompatto in range(len(clusterCompatto)):
        tupla1 = list(cluster[indexElem].values())[0][0]
        tupla2 = list(clusterCompatto[indexCompatto].values())[0][0]
        if tupla1[0]==tupla2[0] and fuzz.token_sort_ratio(tupla1[1],tupla2[1])>75:
            scritto=True
            value1 = list(cluster[indexElem].values())[0]
            value2 = list(clusterCompatto[indexCompatto].values())[0]
            attribute_name = value1[1].union(value2[1])
            attribute_value = value1[2].union(value2[2])
            filename = value1[3].union(value2[3])
            clusterCompatto[indexCompatto][list(clusterCompatto[indexCompatto].keys())[0]]=(tupla2,attribute_name,attribute_value,filename)
            break
    if not scritto:
        clusterCompatto.append(cluster[indexElem])


with open("out_ultima_fase/pozzoCompattoUltimo.txt", "w") as file:
    file.write(str(clusterCompatto))