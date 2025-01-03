from bitarray import bitarray, util
from .utils import PHI, circular_left_shift, subsitution_box_128bits
from random import *

def key_scheduling(key, rondes = 32):
    # key est un bitarray

    if (len(key) > 256):
        raise Exception("Clé trop grande")
    elif (len(key) < 256):
        key += bitarray(256-len(key)) # On complète la clé avec des 0

    k_blocs = []
    # Division en huit blocs de 32 bits
    for i in range(8):
        bloc = key[i*32:(i+1)*32].to01()
        k_blocs.append(int(bloc, 2))

    w_blocs = k_blocs.copy()

    # Expansion de la clé , on récupère 132 sous clés de 32 bits
    for i in range(8, 132):

        xor = w_blocs[i-8] ^ w_blocs[i-5] ^ w_blocs[i-3] ^ w_blocs[i-1] ^ PHI ^ i
        bitshift = circular_left_shift(xor, 11, 32)

        w_blocs.append(bitshift)
    
    cles_de_tour = []
    # Transfo non linéaire
    for i in range(0, rondes+1):
        w0 = w_blocs[i*4]
        w1 = w_blocs[i*4+1]
        w2 = w_blocs[i*4+2]
        w3 = w_blocs[i*4+3]
        
        cle_de_tour = (w0 << 96) | (w1 << 64) | (w2 << 32) | w3
        cles_de_tour.append(subsitution_box_128bits(cle_de_tour))
    
    w_sub = []

    # On recompose en 8 blocs de 32 bits
    for i in range(0,rondes+1):
        cle_de_tour = cles_de_tour[i]   

        w0 = cle_de_tour >> 96
        w1 = (cle_de_tour >> 64) & 0xFFFFFFFF
        w2 = (cle_de_tour >> 32) & 0xFFFFFFFF
        w3 = cle_de_tour & 0xFFFFFFFF

        w_sub.append(w0)
        w_sub.append(w1)
        w_sub.append(w2)
        w_sub.append(w3)

    W_cles = []
    
    for i in range(0,rondes+1):   # On recompose en clés de tour de 128 bits
        W = 0
        for j in range(0,8):    
            Wi = w_sub[4*i] << 96 | w_sub[4*i+1] << 64 | w_sub[4*i+2] << 32 | w_sub[4*i+3]

        W_cles.append(Wi)
    return W_cles,k_blocs
    
def generate_random_key(size = 256): # Génère une clé aléatoire de 128, 192 ou 256 bits
    key = bitarray()

    for i in range(size):
        key.append(randint(0,1))
    
    return key
    

    
    

    




        