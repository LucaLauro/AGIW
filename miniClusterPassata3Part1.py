from fuzzywuzzy import fuzz


with open("miniClusterPassata2.txt", "r") as file:
    miniCluster = eval(file.readline())

listaIndexDaRaggruppare = []
for listaProdotti in miniCluster:
    for tuple in listaProdotti[:-1]:
        nomeAttibuto1 = tuple[0]
        tuplaValueMinuscolo = tuple[1][0][1].lower()
        index1 = listaProdotti.index(tuple)
        for tupleSuccessive in listaProdotti[listaProdotti.index(tuple):]:
            index2 = listaProdotti.index(tupleSuccessive)
            valoriDaVerificare = tupleSuccessive[1][0][1].lower()
            nomeAttibuto2 = tupleSuccessive[0]
            i = fuzz.token_sort_ratio(tuplaValueMinuscolo, valoriDaVerificare)
            i2 = fuzz.ratio(tuplaValueMinuscolo, valoriDaVerificare)
            # i3 = fuzz.token_set_ratio(tuplaValueMinuscolo, valoriDaVerificare)
            if i > 84 and i < 100 and index1 != index2 and nomeAttibuto1 != '<page title>' and not (
                    len(tuplaValueMinuscolo) < 7 and i2 < 50):
                listaIndexDaRaggruppare.append((miniCluster.index(listaProdotti), listaProdotti.index(tuple),
                                                listaProdotti.index(tupleSuccessive)))
                # print(i3)
    print(miniCluster.index(listaProdotti), '/191')

print(listaIndexDaRaggruppare)

with open("miniClusterPassata3Part1.txt", "w") as file:
    file.write(str(listaIndexDaRaggruppare))
