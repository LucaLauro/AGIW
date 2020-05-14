with open("pozzoCompatto.txt", "r") as file:
    pozzo = eval(file.readline())
for elem in pozzo:
    print(elem)