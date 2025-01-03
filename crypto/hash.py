# FONCTION TEMPORAIRE

#import hashlib

#Plus utilisé, utilisé pour les tests
'''def hash(data):
    # Fonction hash
    hashed  =int(hashlib.sha256(data.encode()).hexdigest(), 16)

    return hashed
'''

def custom_hash(data, rounds=4):
    """Implémente un système de hashage basé sur une fonction éponge."""
    # Initialisation de l'état de la fonction éponge
    state = [0] * 16  # 128 bits représentés par 16 octets
    block_size = len(state)

    # Absorption des données
    for byte in data.encode():
        state[0] ^= byte  # Mélange le byte avec l'état initial
        state = sponge_permutation(state, rounds)  # Applique des permutations

    # Squeezing pour générer le hash final
    output = 0
    for i in range(block_size):
        output |= (state[0] << (8 * i))  # Collecte un octet et le place à la position appropriée
        state = sponge_permutation(state, rounds)  # Continue la permutation

    return output  # Retourne le hash sous forme d'entier

def sponge_permutation(state, rounds):
    """Applique des permutations sur l'état pour diffuser les données."""
    for _ in range(rounds):
        # Exemple de permutation : XOR circulaire et rotation
        for i in range(len(state)):
            state[i] ^= (state[(i + 1) % len(state)] + i) & 0xFF
        state = state[-1:] + state[:-1]  # Rotation circulaire
    return state