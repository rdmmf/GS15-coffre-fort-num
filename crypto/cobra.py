from .keys import *
from .utils import *
from .hash import *

import threading

def feistel_f(keys,ronde,X):

    # Étape 1 : Découper le bloc R en blocs de 8 bits, inverser l'ordre des bits et appliquer la fonction inverse.
    Z=0
    for i in range(16):  # 16 blocs de 8 bits dans un bloc de 128 bits
        byte = (X >> (8 * i)) & 0xFF  # Extrait un bloc de 8 bits
        inverted_byte = int(bin(byte)[2:].zfill(8)[::-1], 2)  # Inverse l'ordre des bits
        transformed_byte = ((pow(inverted_byte + 1, -1, 257) - 1) & 0xFF) # Applique la transformation f(x)
        Z |= (transformed_byte << (8 * i))  # Reconstruit le bloc Z.


    # Étape 2 : Mélanger les bits de Z avec une permutation définie.
    p = [7, 5, 3, 1, 0, 2, 4, 6]  # Permutation pour chaque octet
    Y = 0
    for i in range(16):  # 16 blocs de 8 bits
        byte = (Z >> (8 * i)) & 0xFF
        permuted_byte = sum(((byte >> j) & 1) << p[j] for j in range(8))
        Y |= (permuted_byte << (8 * i))


    # Étape 3 : Génération pseudo-aléatoire et mélange avec la clé.
    derived_key = custom_hash(str(keys)) & ((1 << 128) - 1)  # Dérive une clé entière sur 128 bits
    prng_value = Y  # Initialise prng_value avec y pour assurer la réversibilité
    for i in range(16):
        byte = (Y >> (8 * i)) & 0xFF
        seed = (byte ^ ((derived_key >> (8 * (i % 16))) & 0xFF)) & 0xFF  # Combine avec un octet de la clé dérivée
        prng_value ^= (seed << (8 * i))  # Utilise XOR pour garantir la réversibilité

    return prng_value

def feistel_rere_encrypt(bloc, keys, i, ronde_feistel, f_function):
    '''
    Feistel Encryption
    '''
    # On découpe les blocs de 128 bits en deux : L et R
    L = bloc >> 64
    R = bloc & 0xFFFFFFFFFFFFFFFF
    
    for ronde in range(ronde_feistel):
        L1 = R
        R = L ^ f_function(keys,ronde,R)
        L = L1

    result = L << 64
    result += R

    return result

def feistel_rere_decrypt(bloc, keys, i, ronde_feistel, f_function):
    '''
    Feistel Decryption
    '''
    # On découpe les blocs de 128 bits en deux : L et R
    L = bloc >> 64
    R = bloc & 0xFFFFFFFFFFFFFFFF
    
    for ronde in range(ronde_feistel -1,-1,-1):
        R1 = L
        L = R ^ f_function(keys,ronde,L)
        R = R1

    result = L << 64
    result += R

    return result

def cobra_encrypt_thread(blocs, i, W_keys, K_keys, iterations = 32, ronde_feistel = 4):
    bloc = blocs[i] # sous forme de int
    for iteration in range(iterations):
        # XOR avec la clé de tour
        bloc = bloc ^ W_keys[iteration]

        # On applique la S-box
        bloc = subsitution_box_128bits(bloc)

        # Feistel à faire
        bloc = feistel_rere_encrypt(bloc, K_keys, i, ronde_feistel, feistel_f)

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
    '''
    COBRA Encryption (Parallelized)
    '''
    W_keys, K_keys = key_scheduling(key)
    blocs = get_blocs_128bits(data)

    threads = []

    for i in range(len(blocs)):
        threads.append(threading.Thread(target=cobra_encrypt_thread, args=(blocs,i, W_keys, K_keys, iterations, ronde_feistel)))
        threads[i].start()

    # On attend que tous les threads soient terminés
    for thread in threads:
        thread.join()
    
    resultat = 0
    for i in range(len(blocs)):
        resultat = (resultat << 128) | blocs[i]

    return resultat 

def cobra_decrypt_thread(blocs, i, W_keys, K_keys, iterations = 32, ronde_feistel = 4):

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
        bloc = feistel_rere_decrypt(bloc, K_keys, i,ronde_feistel, feistel_f)

        # Substitution box
        bloc = reverse_subsitution_box_128bits(bloc)

        # XOR avec la clé de tour
        bloc = bloc ^ W_keys[iterations-iteration-1]

    blocs[i] = bloc

def cobra_decrypt(key, data, iterations = 32, ronde_feistel = 4, parallelism = 8):
    '''
    COBRA Decryption (Parallelized)
    '''
    W_keys, K_keys = key_scheduling(key)
    blocs = get_blocs_128bits(data)

    threads = []

    for i in range(len(blocs)):
        threads.append(threading.Thread(target=cobra_decrypt_thread, args=(blocs,i, W_keys, K_keys, iterations, ronde_feistel)))
        threads[i].start()

    # On attend que tous les threads soient terminés
    for thread in threads:
        thread.join()
    
    resultat = 0
    for i in range(len(blocs)):
        resultat = (resultat << 128) | blocs[i]

    return resultat  

    
    
    