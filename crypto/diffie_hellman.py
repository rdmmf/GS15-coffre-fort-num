from bitarray import bitarray, util
from .utils import PHI, circular_left_shift, subsitution_box_128bits
from random import *

def generate_public_key (p, g, private_key):
    return pow(g, private_key, p)

def generate_shared_key(private_key, public_key, p):
    return pow(public_key, private_key, p)




if __name__ == "__main__":

    # Un nombre premier
    p = 11476114425077445636913897780729058814788399522553701049280397688323001276391084717487591797788773737035134819088321086678078901084786890698833590212793893
    # Générateur
    g = 5
    # Alice
    a = randint(2, p-1)
    A = generate_public_key(p,g, a)

    # Bob
    b = randint(2, p-1)
    B = generate_public_key(p, g, b)

    shared_key_A = generate_shared_key(a, B, p)
    shared_key_B = generate_shared_key(b, A, p)

    print(shared_key_A == shared_key_B)

