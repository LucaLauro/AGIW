#funzione che prende in input un miniCluster nella forma [[( nome cluster,[(attribute_name, attribute_value, json filename)],..)],..]
#e gli indici di due cluster da unire (il secondo viene copiato nel primo)e l'indice del prodotto a cui appartengono
#e come output fornisce un minicluster dove il cluster principale viene aggiornato con le liste degli attributi di entrambi
# e quello che è stato raggruppato viene sostituito da uno 0
#è necessaria una lista d'appoggio perchè le tuple sono immutabili

def mergeTuple(miniCluster,indexProdotto,indexClusterPrincipale,indexClusterDaRaggruppare):
    listClusterPrinciale = miniCluster[indexProdotto][indexClusterPrincipale][1]
    listClusterDaRaggruppare = miniCluster[indexProdotto][indexClusterDaRaggruppare][1]
    nuovaListaCluster = listClusterPrinciale + listClusterDaRaggruppare
    listaAppoggio = list(miniCluster[indexProdotto][indexClusterPrincipale])
    listaAppoggio[1] = nuovaListaCluster
    miniCluster[indexProdotto][indexClusterPrincipale] = tuple(listaAppoggio)
    miniCluster[indexProdotto][indexClusterDaRaggruppare] = 0
    return miniCluster
