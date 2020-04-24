import json
# mini cluster usando dizionari, problema delle chiavi che non possono essere duplicate, passo ad usare le tuple in miniCluster2.0
counter=0
media = 0
divisore=0
with open("../csvToListOfList.txt", "r") as file:
    prodottiUguali = eval(file.readline())
for prodotti in prodottiUguali:
    dict = {}
    i = 0
    for prodotto in prodotti:
        path = '/Users/luca/PycharmProjects/agiw/venv/data/' + prodotto + ".json"
        f = open(path)
        data = json.load(f)
        for (k, v) in data.items():
            if k != "<page title>" and k not in dict :
                dict.update({k: v})
            if k in dict and v in dict.values():

            i = i+1
        counter=counter+i
    divisore = divisore + 1
    media = media + (i - len(dict))
    print(i-len(dict))


print(divisore)
print(media/divisore)
print(len(dict),i)

