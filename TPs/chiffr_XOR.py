#!/usr/bin/env python3

from bitarray import bitarray
import os, random

# Original message
a = bitarray()
filename =  "rond.png"
with open("files/"+filename, "rb") as f:
    a.fromfile(f)


key = bitarray(0)
input_key = input("Enter the key for encryption >")
key_size = len(input_key)*8

key.frombytes(input_key.encode('utf-8'))

with open("files/"+"key.bin", "wb") as f:
    key.tofile(f)

with open("files/"+"key.bin", "rb") as f:
    key = bitarray()
    key.fromfile(f)


encoded = bitarray()
for i in range(0, len(a)//key_size+1):
    word = a[i*key_size:(i+1)*key_size]
    if len(word) < key_size:
        word += bitarray(key_size-len(word))
    
    encoded.extend(word ^ key)

# Save in a file
with open("files/"+"encrypted_"+filename, "wb") as f:
    encoded.tofile(f)

print("files/rond.png => files/encrypted_rond.png")

key = bitarray(0)
input_key = input("Enter the key for decrypt. >")
key_size = len(input_key)*8
key.frombytes(input_key.encode('utf-8'))

# Load from a file
b = bitarray(0)
with open("files/"+"encrypted_"+filename, "rb") as f:
    b.fromfile(f)


# Decode message
decoded = bitarray()
for i in range(0, len(b)//key_size):
    decoded.extend(b[i*key_size:(i+1)*key_size] ^ key)


# Save in a file
with open("files/"+"decoded_"+filename, "wb") as f:
    decoded.tofile(f)


print("files/encrypted_rond.png => files/decoded_rond.png")
