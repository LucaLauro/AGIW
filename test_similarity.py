from fuzzywuzzy import fuzz

print(fuzz.token_set_ratio("battery type", "screen type"))
print(fuzz.token_set_ratio("battery type", "type"))
print(fuzz.token_set_ratio("battery ", "battery type"))
print(fuzz.token_set_ratio("battery ", "battery rechargeable"))
print(fuzz.token_set_ratio("battery", "battery chemistry"))
print("---------------")

print(fuzz.partial_ratio("battery type", "screen type"))
print(fuzz.partial_ratio("battery type", "type"))
print(fuzz.partial_ratio("battery ", "battery type"))
print(fuzz.partial_ratio("battery ", "battery rechargeable"))
print(fuzz.partial_ratio("battery", "battery chemistry"))
print("---------------")

print(fuzz.ratio("battery type", "screen type"))
print(fuzz.ratio("battery type", "type"))
print(fuzz.ratio("battery", "battery type"))
print(fuzz.ratio("battery", "battery rechargeable"))
print(fuzz.ratio("battery", "battery chemistry"))



