from fuzzywuzzy import fuzz
print(fuzz.token_sort_ratio('sensor size','screen size'))
print(fuzz.ratio('sensor size','screen size'))
print(fuzz.token_set_ratio('sensor size','screen size'))
print(fuzz.token_sort_ratio('effective megapixels','megapixels'))
print(fuzz.ratio('effective megapixels','megapixels'))
print(fuzz.token_set_ratio('bran','brand'))
counter=0
