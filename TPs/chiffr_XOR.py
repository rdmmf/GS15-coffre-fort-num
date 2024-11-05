#!/usr/bin/env python3

from bitarray import bitarray
import os, random

key = bitarray(0)
input_key = input("Enter the key >")
key_size = len(input_key)*8

key.frombytes(input_key.encode('utf-8'))
print("KEY :",key.tobytes().decode('latin-1'))

with open("key.bin", "wb") as f:
    key.tofile(f)

with open("key.bin", "rb") as f:
    key = bitarray()
    key.fromfile(f)

# Original message
a = bitarray()
message = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
print("MESSAGE : ",message)
# Encode message
a.frombytes(message.encode('utf-8'))

encoded = bitarray()
for i in range(0, len(a)//key_size+1):
    word = a[i*key_size:(i+1)*key_size]
    if len(word) < key_size:
        word += bitarray(key_size-len(word))
    
    encoded.extend(word ^ key)
print(len(encoded))

print("SAVE ENCODED MSG : ",encoded.to01())
# Save in a file
with open("test.bin", "wb") as f:
    encoded.tofile(f)

key = bitarray(0)
input_key = input("Enter the key >")
key_size = len(input_key)*8
key.frombytes(input_key.encode('utf-8'))

# Load from a file
b = bitarray(0)
with open("test.bin", "rb") as f:
    b.fromfile(f)


print("OPEN ENCODED MSG : ",b.to01())
# Decode message
decoded = bitarray()
for i in range(0, len(b)//key_size):
    decoded.extend(b[i*key_size:(i+1)*key_size] ^ key)

print("UNDECODED :",decoded.tobytes().decode('utf-8'))