# [[( nome cluster,[(attribute_name, attribute_value, json filename)],..)],..]
import json

with open("csvToListOfList.txt", "r") as file:
    prodottiUguali = eval(file.readline())
miniCluster = []
for prodotti in prodottiUguali:
    clusterListStessiProdotti = [] #creo una lista di appoggio per poi inserirla nella lista definitiva
    for prodotto in prodotti:
        path = 'data/' + prodotto + ".json"   #carico il file del prodotto
        f = open(path)
        data = json.load(f)
        for (k, v) in data.items():   #itero ogni attributo del prodotto
            nonTrovato = True
            if '(more than' in v:     #elimino i (more than xx%) che danno fastidio
                i = v.index('(')
                v = v[:i]
            if type(v) == list:
                v = str(v).strip('[]')  #elimino i caratteri [ ] che mi farebbero sbagliare in fasi successiva l'elaborazione del tipo del valore(in sostanza lo elaborava come una lista invece che come una stringa
            for cluster in clusterListStessiProdotti:    #itero i cluster nella lista di appoggio(sono tutti dello stesso prodotto)
                if k == cluster[1][0][0] and v == cluster[1][0][1]: #se il cluster dell'attrubuto preso in considerazione esiste già faccio l'append dell'attributo in considerazione
                    cluster[1].append((k, v, prodotto + "/" +k))
                    nonTrovato = False   #uso una variabile booleana per indicare se ho trovato un cluster in cui inserire l'attributo altrimenti ne creo un altro nuovo
            if nonTrovato:
                clusterListStessiProdotti.append((k, [(k, v, prodotto + "/" +k)]))
        f.close()
    miniCluster.append(clusterListStessiProdotti)   #inserisco la lista d'appoggio in quella definitiva

with open("miniClusterPassata1.txt", "w") as file:
    file.write(str(miniCluster))