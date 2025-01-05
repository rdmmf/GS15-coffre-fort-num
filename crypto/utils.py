from bitarray.util import ba2int, int2ba, bitarray
import random

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
    """
    Génère les inverses des S-Boxes fournies.
    """
    reversed_sboxes = []
    for sbox in sboxes:
        inverse_sbox = [0] * len(sbox)  # Initialize an array of the same size as the S-box
        for i, value in enumerate(sbox):
            inverse_sbox[value] = i  # Reverse the mapping
        reversed_sboxes.append(inverse_sbox)
    return reversed_sboxes

def circular_left_shift(value, shift, bit_size):
    """
    Effectue une rotation circulaire à gauche.
    """
    return ((value << shift) | (value >> (bit_size - shift))) & ((1 << bit_size) - 1)

def circular_right_shift(value, shift, bit_size):
    '''
    Effectue une rotation circulaire à droite.
    '''
    return ((value >> shift) | (value << (bit_size - shift))) & ((1 << bit_size) - 1)

def left_shift(value, shift, bit_size):
    '''
    Effectue un décalage à gauche.
    '''
    return (value << shift) & ((1 << bit_size) - 1)

def right_shift(value, shift, bit_size):
    '''
    Effectue un décalage à droite.
    '''
    return (value >> shift) & ((1 << bit_size) - 1)

def subsitution_box_4bits(bloc, sbox):
    '''
    Applique une substitution via une S-Box sur un bloc de 4 bits.
    '''
    # Si c'est un bit array
    if isinstance(bloc, bitarray):
        bloc = ba2int(bloc)  # Convertir les bits en entier pour chercher dans la S-Box

    substitution = sbox[bloc]  # Appliquer la S-box

    return substitution

def subsitution_box_128bits(bloc, sboxes = S_BOXES):
    '''
    Applique des S-Boxes sur un bloc de 128 bits, 4 bits à la fois.
    '''
    # Si c'est un bit array
    if isinstance(bloc, bitarray):
        bloc = ba2int(bloc)  # Convertir les bits en entier pour chercher dans la S-Box

    substitution = 0

    for i in range(0,32): # Parcourt 32 segments de 4 bits dans le bloc

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
    '''
    Découpe les données en blocs de 128 bits.
    '''
    if isinstance(data, int):
        data = int2ba(data)
    # On découpe les données en blocs de 128 bits
    padding_length = (128 - len(data) % 128) % 128
    data = bitarray('0' * padding_length) + data

    # Découpe le bitarray en blocs de 128 bits
    blocs = [ ba2int( data[i:i + 128] ) for i in range(0, len(data), 128)]

    return blocs

def get_blocs_64bits(data):
    '''
    Découpe les données en blocs de 64 bits.
    '''
    if isinstance(data, int):
        data = int2ba(data)
    # On découpe les données en blocs de 64 bits
    padding_length = (64 - len(data) % 64) % 64
    data = bitarray('0' * padding_length) + data

    # Découpe le bitarray en blocs de 64 bits
    blocs = [ ba2int( data[i:i + 64] ) for i in range(0, len(data), 64)]

    return blocs

def get_blocs_1024bits(data):
    '''
    Découpe les données en blocs de 1024 bits.
    '''
    if isinstance(data, int):
        data = int2ba(data)
    # On découpe les données en blocs de 1024 bits
    padding_length = (1024 - len(data) % 1024) % 1024
    data = bitarray('0' * padding_length) + data

    # Découpe le bitarray en blocs de 1024 bits
    blocs = [ ba2int( data[i:i + 1024] ) for i in range(0, len(data), 1024)]

    return blocs

def get_array_from_int(encoded_int):

    bitarr = int2ba(encoded_int)

    if len(bitarr) % 8 != 0:
        padding_length = 8 - (len(bitarr) % 8)
        bitarr = bitarray('0' * padding_length) + bitarr
    
    return bitarr

def PGCD(a, b):
    '''
    Calcule le plus grand commun diviseur (PGCD) de deux nombres.
    '''
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    '''
    Calcule l'inverse modulaire de e mod phi via l'algorithme étendu d'Euclide.
    '''
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
    '''
    Teste si un nombre est premier
    '''
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_prime_miller_rabin(n, k=50):
    '''
    Teste si un nombre est premier avec le test de Miller-Rabin.
    - n : Nombre à tester
    - k : Nombre d'itérations du test
    '''
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
        a = random.randint(2, n - 2)
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

def generate_prime(nb_bits, seed):
    '''
    Génère un nombre premier de nb_bits bits en utilisant une graine.
    '''
    random.seed(seed)
    while True:
        x = random.getrandbits(nb_bits) | 1  # Pour s'assurer qu'il est impair
        if is_prime_miller_rabin(x):
            return x
        
def print_int_to_string(x):
    '''
    Convertit un entier en chaîne.
    '''
    try: 
        return get_array_from_int(x).tobytes().decode("latin-1")
    except:
        return get_array_from_int(x).to01()
    
def string_to_int(s):
    '''
    Convertit une chaîne en un entier.
    '''
    s_bytes = s.encode("latin-1")
    return int.from_bytes( s_bytes, byteorder='big')

        
REVERSED_S_BOXES = generate_inverse_sboxes(S_BOXES)