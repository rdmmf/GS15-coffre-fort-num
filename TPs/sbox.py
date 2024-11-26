from bitarray import bitarray
from bitarray.util import ba2int, int2ba

# Fonction pour créer des S-Boxes personnalisées
def generate_sboxes():
    sboxes = []
    for i in range(4):  # On génère 4 S-Boxes
        sbox = [((x * 3 + i) % 16) for x in range(16)]  # Exemple simple de transformation
        sboxes.append(sbox)
    return sboxes

# Appliquer une S-Box donnée sur une entrée de 4 bits
def apply_sbox(input_bits, sbox):
    index = ba2int(input_bits)  # Convertir les bits en entier pour chercher dans la S-Box
    output = int2ba(sbox[index], length=4)  # Récupérer la sortie correspondante
    return output

# Fonction principale pour appliquer les S-Boxes sur un bloc de 128 bits
def substitute(block):
    if len(block) != 128:
        raise ValueError("Le bloc doit faire exactement 128 bits.")

    sboxes = generate_sboxes()
    substituted = bitarray()

    for i in range(32):  # 32 segments de 4 bits
        segment = block[i * 4:(i + 1) * 4]  # Extraire un segment de 4 bits
        sbox_index = i // 8  # Sélectionner la S-Box (0 à 7 -> 0, 8 à 15 -> 1, etc.)
        substituted += apply_sbox(segment, sboxes[sbox_index])  # Appliquer la S-Box correspondante

    return substituted

from bitarray import bitarray
from bitarray.util import ba2int, int2ba

# Fonction pour créer des S-Boxes inversées
def generate_inverse_sboxes(sboxes):
    inverse_sboxes = []
    for sbox in sboxes:
        inverse_sbox = [0] * 16
        for input_val, output_val in enumerate(sbox):
            inverse_sbox[output_val] = input_val
        inverse_sboxes.append(inverse_sbox)
    return inverse_sboxes

# Appliquer une S-Box inversée sur une entrée de 4 bits
def apply_inverse_sbox(input_bits, inverse_sbox):
    index = ba2int(input_bits)  # Convertir les bits en entier pour chercher dans la S-Box inverse
    output = int2ba(inverse_sbox[index], length=4)  # Récupérer la sortie correspondante
    return output

# Fonction principale pour appliquer l'inverse des S-Boxes sur un bloc de 128 bits
def reverse_substitute(block, sboxes):
    if len(block) != 128:
        raise ValueError("Le bloc doit faire exactement 128 bits.")

    inverse_sboxes = generate_inverse_sboxes(sboxes)
    reversed_block = bitarray()

    for i in range(32):  # 32 segments de 4 bits
        segment = block[i * 4:(i + 1) * 4]  # Extraire un segment de 4 bits
        sbox_index = i // 8  # Sélectionner la S-Box inverse (0 à 7 -> 0, 8 à 15 -> 1, etc.)
        print(i,sbox_index)
        reversed_block += apply_inverse_sbox(segment, inverse_sboxes[sbox_index])  # Appliquer la S-Box inverse

    return reversed_block

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple de bloc de 128 bits
    input_block = bitarray("1010101111001101111011110000110011110000110011111010101010101111" * 2)
    
    # Générer les S-Boxes
    sboxes = generate_sboxes()

    print("S-Boxes:")
    print(len(sboxes))

    # Appliquer la substitution
    substituted_block = substitute(input_block)
    
    # Inverser la substitution
    reversed_block = reverse_substitute(substituted_block, sboxes)
    
    print("Bloc d'entrée:      ", input_block)
    print("Bloc substitué:     ", substituted_block)
    print("Bloc inversé:       ", reversed_block)
    print("Inversion réussie ? ", input_block == reversed_block)
