from bitarray.util import ba2int, int2ba, bitarray
from random import *

# CONSTANTES

PHI = 0x9E3779B9
S_BOXES = [
    [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7],
    [0xF, 0x1, 0x8, 0xE, 0x6, 0xB, 0x3, 0x4, 0x9, 0x7, 0x2, 0xD, 0xC, 0x0, 0x5, 0xA],
    [0xA, 0x0, 0x9, 0xE, 0x6, 0x3, 0xF, 0x5, 0x1, 0xD, 0xC, 0x7, 0xB, 0x4, 0x2, 0x8],
    [0x7, 0xE, 0x4, 0xB, 0x2, 0x8, 0xF, 0xD, 0x1, 0xA, 0x6, 0xC, 0x5, 0x9, 0x3, 0x0],
]

REVERSED_S_BOXES = []

def generate_inverse_sboxes(sboxes):
    reversed_sboxes = []
    for sbox in sboxes:
        inverse_sbox = [0] * len(sbox)  # Initialize an array of the same size as the S-box
        for i, value in enumerate(sbox):
            inverse_sbox[value] = i  # Reverse the mapping
        reversed_sboxes.append(inverse_sbox)
    return reversed_sboxes

def circular_left_shift(value, shift, bit_size):
    
    return ((value << shift) | (value >> (bit_size - shift))) & ((1 << bit_size) - 1)

def circular_right_shift(value, shift, bit_size):
    
    return ((value >> shift) | (value << (bit_size - shift))) & ((1 << bit_size) - 1)

def left_shift(value, shift, bit_size):
    
    return (value << shift) & ((1 << bit_size) - 1)

def right_shift(value, shift, bit_size):
        
    return (value >> shift) & ((1 << bit_size) - 1)

def subsitution_box_4bits(bloc, sbox):

    # Si c'est un bit array
    if isinstance(bloc, bitarray):
        bloc = ba2int(bloc)  # Convertir les bits en entier pour chercher dans la S-Box

    substitution = sbox[bloc]  # Appliquer la S-box

    return substitution

def subsitution_box_128bits(bloc, sboxes = S_BOXES):

    # Si c'est un bit array
    if isinstance(bloc, bitarray):
        bloc = ba2int(bloc)  # Convertir les bits en entier pour chercher dans la S-Box

    substitution = 0

    for i in range(0,32):

        # Selectionner parmis les 4 s-boxes
        if (i < 8):
            sbox = sboxes[0]
        elif (i < 16):
            sbox = sboxes[1]
        elif (i < 24):
            sbox = sboxes[2]
        elif (i < 32):
            sbox = sboxes[3]
        else:
            raise Exception("Index de S-box invalide")

        segment = bloc >> (i*4) & 0xF

        substitution += subsitution_box_4bits(segment, sbox) << (i*4)

    return substitution

def reverse_subsitution_box_128bits(bloc):
    return subsitution_box_128bits(bloc, REVERSED_S_BOXES)

def get_blocs_128bits(data):
    if isinstance(data, int):
        data = int2ba(data)
    # On découpe les données en blocs de 128 bits
    padding_length = (128 - len(data) % 128) % 128
    data = bitarray('0' * padding_length) + data

    # Découpe le bitarray en blocs de 128 bits
    blocs = [ ba2int( data[i:i + 128] ) for i in range(0, len(data), 128)]

    return blocs

def get_array_from_int(encoded_int):

    bitarr = int2ba(encoded_int)

    if len(bitarr) % 8 != 0:
        padding_length = 8 - (len(bitarr) % 8)
        bitarr = bitarray('0' * padding_length) + bitarr
    
    return bitarr

def PGCD(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    original_phi = phi
    x0, x1 = 0, 1
    while e > 1:
        q = e // phi
        e, phi = phi, e % phi
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += original_phi
    return x1


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_prime_miller_rabin(n, k=50):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # On teste k fois
    for _ in range(k):
        a = randint(2, n - 2)
        x = pow(a, d, n)  
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(nb_bits):
    while True:
        x = getrandbits(nb_bits) | 1  # Pour s'assurer qu'il est impair
        if is_prime_miller_rabin(x):
            return x

        
REVERSED_S_BOXES = generate_inverse_sboxes(S_BOXES)