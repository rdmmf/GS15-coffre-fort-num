from crypto.keys import *
from crypto.utils import *

def feistel_f(x):
    # Prend un entier 256 bits
    # Retourne un entier 256 bits
    
    pass # Je sais pas faire 

def cobra_encrypt(key, data, iterations = 32, ronde_feistel = 4):
    
    keys = key_scheduling(key)
    
    # On découpe les données en blocs de 128 bits
    blocs_init = []
    for i in range(0,len(data)//128+1):

        if (i+1)*128 > len(data): # Si on dépasse la taille des données, on complète avec des 0
            bloc_init = data[i*128:]
            bloc_init += bitarray(128-len(bloc_init))

        else:
            bloc_init = data[i*128:(i+1)*128]

        blocs_init.append( ba2int(bloc_init) )

    blocs = blocs_init.copy()


    for iteration in range(iterations):
        # XOR avec la clé de tour
        for i in range(len(blocs)):
            bloc = blocs[i]
            blocs[i] = bloc ^ keys[iteration]

        # On applique la S-box
        for i in range(len(blocs)):
            blocs[i] = subsitution_box_128bits(blocs[i])

        # Feistel

        # Transfo linéaire



    ###### VERIFICIATION QUE CE SOIT DECHIFFRABLE ######
    # A RETIRER QUAND LA FONCTION EST FINIE
    for iteration in range(iterations):
        for i in range(len(blocs)):
            blocs[i] = reverse_subsitution_box_128bits(blocs[i])
        for i in range(len(blocs)):
            bloc = blocs[i]
            blocs[i] = bloc ^ keys[iterations-iteration-1]
    print("A-t-on réussi à reverse le msg chiffré ? :" ,blocs_init == blocs)
    ####################################################
        

        

    
    
    