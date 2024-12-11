from crypto.keys import *
from crypto.utils import *

import threading

def feistel_f(x):
    # Prend un entier 256 bits
    # Retourne un entier 256 bits
    return x # TEMPOIRAIRE

def cobra_encrypt_thread(blocs, i, keys, iterations = 32, ronde_feistel = 4):
    bloc = blocs[i]
    for iteration in range(iterations):
        # XOR avec la clé de tour
        bloc = bloc ^ keys[iteration]

        # On applique la S-box
        bloc = subsitution_box_128bits(bloc)

        # Feistel à faire


        # Transfo linéaire
        # On récupère les blocs de 32 bits
        a = bloc >> 96
        b = bloc >> 64 & 0xFFFFFFFF
        c = bloc >> 32 & 0xFFFFFFFF
        d = bloc & 0xFFFFFFFF

        a = circular_left_shift(a, 13, 32)
        c = circular_left_shift(c, 3, 32)
        
        b = b ^ a ^ c
        d = d ^ left_shift(a,3,32) ^ c

        b = circular_left_shift(b, 1, 32)
        d = circular_left_shift(d, 7, 32)

        a = a ^ b ^ d
        c = c ^ left_shift(b,7,32) ^ d

        a = circular_left_shift(a, 5, 32)
        c = circular_left_shift(c, 22, 32)

        # On recombine les blocs
        bloc = (a << 96) | (b << 64) | (c << 32) | d

    blocs[i] = bloc

def cobra_encrypt(key, data, iterations = 32, ronde_feistel = 4):
    
    keys = key_scheduling(key)
    blocs = get_blocs_128bits(data)

    threads = []

    for i in range(len(blocs)):
        threads.append(threading.Thread(target=cobra_encrypt_thread, args=(blocs,i, keys, iterations, ronde_feistel)))
        threads[i].start()

    # On attend que tous les threads soient terminés
    for thread in threads:
        thread.join()
    
    resultat = 0
    for i in range(len(blocs)):
        resultat = (resultat << 128) | blocs[i]

    return resultat 

def cobra_decrypt_thread(blocs, i, keys, iterations = 32, ronde_feistel = 4):

    bloc = blocs[i]
    for iteration in range(iterations):
        # On récupère les blocs de 32 bits
        a = bloc >> 96
        b = bloc >> 64 & 0xFFFFFFFF
        c = bloc >> 32 & 0xFFFFFFFF
        d = bloc & 0xFFFFFFFF

        # Transfo linéaire
        c = circular_right_shift(c, 22, 32)
        a = circular_right_shift(a, 5, 32)

        c = c ^ (left_shift(b,7,32) ^ d)
        a = a ^ (b ^ d)

        d = circular_right_shift(d, 7, 32)
        b = circular_right_shift(b, 1, 32)

        d = d ^ left_shift(a,3,32) ^ c
        b = b ^ (a ^ c)

        c = circular_right_shift(c, 3, 32)
        a = circular_right_shift(a, 13, 32)

        # On recombine les blocs
        bloc = (a << 96) | (b << 64) | (c << 32) | d

        # Feistel à faire


        # Substitution box
        bloc = reverse_subsitution_box_128bits(bloc)

        # XOR avec la clé de tour
        bloc = bloc ^ keys[iterations-iteration-1]

    blocs[i] = bloc

def cobra_decrypt(key, data, iterations = 32, ronde_feistel = 4, parallelism = 8):

    keys = key_scheduling(key)
    blocs = get_blocs_128bits(data)

    threads = []

    for i in range(len(blocs)):
        threads.append(threading.Thread(target=cobra_decrypt_thread, args=(blocs,i, keys, iterations, ronde_feistel)))
        threads[i].start()

    # On attend que tous les threads soient terminés
    for thread in threads:
        thread.join()
    
    resultat = 0
    for i in range(len(blocs)):
        resultat = (resultat << 128) | blocs[i]

    return resultat  

    
    
    