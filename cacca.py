from fuzzywuzzy import fuzz

print(fuzz.token_sort_ratio('1/2.3 inches','3"'))
print(fuzz.token_sort_ratio('1/2.3 inches','3 inches'))