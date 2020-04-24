# prendo 1 prodotto e tutti quelli uguali
# prendo tutti i valori e gli toglo le maiuscole e le minuscole
# raccolgo solo quelli con 1 parola(separati da _ o da " ") e li metto  in un dict
# controllo se ci sono attributi che compaiono meno volte della metà dei prodotti e se posso inglobarla in un attributo che compare più volte della metà dei prodotti
# inserisco in un dizionario che le due parole significano la stessa cosa
# poi prendo quelli con 2 parole, se non esistono entrambe passo avanti, invece se una delle 2 esiste controllo che il vaolre dell'attributo appena preso in esame sia presente in altri attributi che hanno una delle due parole. se è presente l'attributo con + parole sapà più specifico, (controllare questo pezzo)->se non sono presenti potrebbero essere dettagli informativi
# poi controllo se sono presenti "errori di battitutra" quindi posso eliminare tutti i spazi i valori e verificare quanto i vari attributi siano uguali tra di loro, se cambiano massimo 1 o 2 caratteri sono la stessa cosa(almeno la stringsa deve essere di 4 caratteri così elimino i valori yes e no)



#prendo tutti gli attributi di prodotti uguali e se sono uguali sia il nome attributo che il valore li unisco insieme e gli assegno un valore che dice quanti ne ho uniti
#poi passo a controllare i valori e controllo se ci sono dei valori uguali con nomi di attributi diversi-> controllo nella ground truth se indicano la stessa cosa
#inserisco in un dizionario i nomi degli attributi che indicano la stessa cosa e inizio a formare un dict che userò per l'intero dataset
#
#
#
#