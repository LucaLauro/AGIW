s='battery type'
x='battery chemistry'
data=s.split(' ')
print(set(data))
data2=x.split(' ')
print(len(set(data).intersection(set(data2)))>0)