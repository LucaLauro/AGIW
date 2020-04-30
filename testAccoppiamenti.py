from fuzzywuzzy import fuzz

with open("miniClusterRaggruppato.txt", "r") as file:
    miniCluster = eval(file.readline())

#for tuple in miniCluster[190]:
 #   if tuple!=0:
  #      print(tuple)

int=0
int2=0
for tuple in miniCluster[188][:-1]:
    nomeAttibuto1=tuple[0]
    tuplaValueMinuscolo=tuple[1][0][1].lower()
    index1=miniCluster[188].index(tuple)
    for tupleSuccessive in miniCluster[188][miniCluster[188].index(tuple):]:
        valoriDaVerificare=tupleSuccessive[1][0][1].lower()
        nomeAttibuto2=tupleSuccessive[0]

        #if fuzz.token_set_ratio(valoriDaVerificare,'(more than') ==100:
        #    posizione=valoriDaVerificare.index('(')
        #    valoriDaVerificare=valoriDaVerificare[:posizione]
        #if fuzz.token_set_ratio(tuplaValueMinuscolo,'(more than') ==100:
        #    posizione2 = tuplaValueMinuscolo.index('(')
        #    tuplaValueMinuscolo = tuplaValueMinuscolo[:posizione2]

        i = fuzz.token_sort_ratio(tuplaValueMinuscolo, valoriDaVerificare)
        i2 = fuzz.ratio(tuplaValueMinuscolo, valoriDaVerificare)
        i3 = fuzz.token_set_ratio(tuplaValueMinuscolo, valoriDaVerificare)
        index2 = miniCluster[188].index(tupleSuccessive)

        if i>84 and i<100 and index1!=index2 and nomeAttibuto1!='<page title>' and not (len(tuplaValueMinuscolo)<7 and i2<50):
            print(tuplaValueMinuscolo+'---'+nomeAttibuto1,index1)
            print(valoriDaVerificare+'---'+nomeAttibuto2,index2)
            print(i)
            print(i2)
            print(i3)
            int=int+1

        """if i > 70 and i < 80 and index1 != index2 and nomeAttibuto1 != '<page title>':
            int2=int2+1
            print(tuplaValueMinuscolo+'---'+ nomeAttibuto1, index1)
            print(valoriDaVerificare+'---'+nomeAttibuto2, index2)
            print(i)
            print(i2)
            print(i3)"""
print(int,int2,len(miniCluster[188]))
print(miniCluster[188])