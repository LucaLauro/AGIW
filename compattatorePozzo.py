from fuzzywuzzy import fuzz
with open("ground_truth/pozzo8.txt", "r") as file:
    pozzo = eval(file.readline())

pozzoCompatto=[]
indexUsati=[]

for indexElem in range((len(pozzo)-1)):
    scritto=False
    print(inde)

    for indexSuccessivo in range(indexElem+1,(len(pozzo))):
        tupla1=list(pozzo[indexElem].values())[0][0]
        tupla2=list(pozzo[indexSuccessivo].values())[0][0]
        if tupla1[0]==tupla2[0] and indexElem not in indexUsati and indexSuccessivo not in indexUsati:
            if fuzz.token_sort_ratio(tupla1[1],tupla2[1])>75:

                value1=list(pozzo[indexElem].values())[0]

                value2=list(pozzo[indexSuccessivo].values())[0]
                attribute_name = value1[1].union(value2[1])
                attribute_value = value1[2].union(value2[2])
                filename = value1[3].union(value2[3])
                #print(attribute_name)
                #print(attribute_value)
                #print(filename)
                if scritto:

                    pozzoCompatto[len(pozzoCompatto)-1][list(pozzo[indexElem].keys())[0]]=(tupla1,attribute_name,attribute_value,filename)
                else:
                    pozzoCompatto.append({list(pozzo[indexElem].keys())[0]:(tupla1,attribute_name,attribute_value,filename)})
                    scritto=True
                indexUsati.append(indexSuccessivo)
    if not scritto and indexElem not in indexUsati:
        pozzoCompatto.append(pozzo[indexElem])
print(len(pozzo))
print(len(pozzoCompatto))

with open("pozzoCompatto1.txt", "w") as file:
    file.write(str(pozzoCompatto))
