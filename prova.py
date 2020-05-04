import math
from fuzzywuzzy import fuzz
print(fuzz.token_sort_ratio('sensor size','screen size'))
print(fuzz.ratio('sensor size','screen size'))
print(fuzz.token_set_ratio('sensor size','screen size'))
print(fuzz.token_sort_ratio('digital slr','slr'))
print(fuzz.ratio('effective megapixels','megapixels'))
print(fuzz.token_set_ratio('bran','brand'))
counter=0
for i in range(10):
    counter=counter+i
print(counter)
print(math.pow(10000,2))
print(math.log10(10000))
print(10000*(math.log10(10000)))