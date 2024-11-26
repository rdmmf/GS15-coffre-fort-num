
from crypto.keys import key_scheduling
from crypto.utils import subsitution_box_128bits, reverse_subsitution_box_128bits
from bitarray.util import int2ba, ba2int
from crypto.algo import cobra_encrypt, feistel_f

from bitarray import bitarray, util
import random

if __name__ == "__main__":
    input_key = bitarray()
    for i in range(128):
        input_key.append(random.getrandbits(1))
    print("Key : ",ba2int(input_key))

    input_key  = ba2int(input_key)
    sbox = subsitution_box_128bits(input_key)
    print("Sbox : ",sbox)
    reversed_sbox = reverse_subsitution_box_128bits(sbox)
    print("Reversed Sbox : ",reversed_sbox)
    print(input_key == reversed_sbox)
    
    # Cle random de 256 bits
    input_key = bitarray()
    for i in range(256):
        input_key.append(random.getrandbits(1))
    print("Key : ",ba2int(input_key))

    # On génère les sous clés
    subkeys = key_scheduling(input_key)

    print("On récupère n clés : ",len(subkeys))

    # data = bitarray()
    # # Ouvrir le fichier avec bitarray
    # with open("TPs/files/rond.png", "rb") as f:
    #     data = bitarray()
    #     data.fromfile(f)

    data = bitarray()
    for i in range(3000):
        data.append(random.getrandbits(1))

    cobra_encrypt(input_key, data)

    for i in range(300):
        y = feistel_f(i)
        print("Feistel f de ",i," : ",y)
        print("len : ",len(int2ba(y)))

