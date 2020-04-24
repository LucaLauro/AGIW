import json


with open("../csvToListOfList.txt", "r") as file:
    prodottiUguali = eval(file.readline())

dict = {}
i = 0
for prodotto in prodottiUguali[188]:
    path = '/Users/luca/PycharmProjects/agiw/venv/data/' + prodotto + ".json"
    f = open(path)
    data = json.load(f)
    for (k, v) in data.items():
        if k != "<page title>" and k not in dict:
            dict.update({k: v})
        i = i+1

print(len(prodottiUguali[188]))
print(dict)
print(len(dict),i)
