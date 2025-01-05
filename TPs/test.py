import bitarray

a = bitarray.bitarray()
b = bitarray.bitarray()

with open("data/client/test.txt", "rb") as file:
    a.fromfile(file)

with open("data/client/output.txt", "rb") as file:
    b.fromfile(file)

print(len(a))
print(len(b))
print(a == b)
