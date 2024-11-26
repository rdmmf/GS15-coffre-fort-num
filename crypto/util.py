from bitarray.util import ba2int, int2ba, bitarray
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
    inverse_sboxes = []
    
    for sbox in sboxes:
        
        inverse_sbox = [0] * 16
        
        for input_val, output_val in enumerate(sbox):
            
            inverse_sbox[output_val] = input_val
        
        inverse_sboxes.append(inverse_sbox)
    
    return inverse_sboxes

def circular_left_shift(value, shift, bit_size):
    
    return ((value << shift) | (value >> (bit_size - shift))) & ((1 << bit_size) - 1)

def circular_right_shift(value, shift, bit_size):
    
    return ((value >> shift) | (value << (bit_size - shift))) & ((1 << bit_size) - 1)

def subsitution_box_4bits(bloc, sbox):

    # Si c'est un bit array
    if isinstance(bloc, bitarray):
        bloc = ba2int(bloc)  # Convertir les bits en entier pour chercher dans la S-Box

    substitution = sbox[bloc]  # Appliquer la S-box

    return substitution

def subsitution_box_128bits(bloc):

    # Si c'est un bit array
    if isinstance(bloc, bitarray):
        bloc = ba2int(bloc)  # Convertir les bits en entier pour chercher dans la S-Box

    substitution = 0

    for i in range(0,32):

        # Selectionner parmis les 4 s-boxes
        if (i < 8):
            sbox = S_BOXES[0]
        elif (i < 16):
            sbox = S_BOXES[1]
        elif (i < 24):
            sbox = S_BOXES[2]
        elif (i < 32):
            sbox = S_BOXES[3]
        else:
            raise Exception("Index de S-box invalide")

        segment = bloc >> (i*4) & 0xF

        substitution += subsitution_box_4bits(segment, sbox) << (i*4)

    return substitution

REVERSED_S_BOXES = generate_inverse_sboxes(S_BOXES)