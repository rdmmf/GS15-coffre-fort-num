from bitarray import bitarray, util
from crypto.utils import PHI, circular_left_shift, subsitution_box_128bits
from random import *

def public_key (g, p, private_key):
    return pow(g, private_key, p)

def shared_key(private_key, public_key, p):
    return pow(public_key, private_key, p)




def main():

    # Un nombre premier
    p = 11476114425077445636913897780729058814788399522553701049280397688323001276391084717487591797788773737035134819088321086678078901084786890698833590212793893
    # Générateur
    g = 5
    # Alice
    a = randint(2, p-1)
    A = public_key(g, p, a)

    # Bob
    b = randint(2, p-1)
    B = public_key(g, p, b)

    shared_key_A = shared_key(a, B, p)
    shared_key_B = shared_key(b, A, p)

    print(shared_key_A == shared_key_B)