import crypto.keys
from crypto.keys import key_scheduling

from bitarray import bitarray, util
import random

if __name__ == "__main__":
    from bitarray.util import int2ba
    
    # Cle random de 256 bits
    input_key = bitarray()
    for i in range(256):
        input_key.append(random.getrandbits(1))
        

    subkeys = key_scheduling(input_key)

    print(subkeys)
    print("On récupère n clés : ",len(subkeys))
    
    for i in range(0,33):
        print("Clé ",i,": ", len(int2ba(subkeys[i])))