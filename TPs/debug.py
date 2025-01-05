
from crypto.keys import key_scheduling, generate_random_key
from crypto.utils import subsitution_box_128bits, reverse_subsitution_box_128bits, get_blocs_128bits, get_array_from_int
from bitarray.util import int2ba, ba2int
from crypto.cobra import cobra_encrypt, feistel_f, cobra_decrypt
from crypto.hash import custom_hash
from bitarray import bitarray, util
import random, time
import logging_config, logging
from crypto.rsa import guillou_quisquater_protocol, test_rsa_encrypt_decrypt, test_rsa_encrypt_decrypt_64bits

from crypto.hash import custom_hash

import services

if __name__ == "__main__":

    logging_config.init_logging()

    logger = logging.getLogger(__name__)
    print("Guillou quisquater protocol signature ZKP : ")
    #guillou_quisquater_protocol()

    print("RSA Encrypt Decrypt : ")
    test_rsa_encrypt_decrypt()
    #test_rsa_encrypt_decrypt_64bits()

    input_key = bitarray()
    for i in range(128):
        input_key.append(random.getrandbits(1))
    print("Key : ",ba2int(input_key))

    input_key  = ba2int(input_key)
    sbox = subsitution_box_128bits(input_key)
    print("Sbox : ",sbox)
    reversed_sbox = reverse_subsitution_box_128bits(sbox)
    print("Reversed Sbox : ",reversed_sbox)
    print(input_key == reversed_sbox)
    
    # Cle random de 256 bits
    input_key = bitarray()
    for i in range(256):
        input_key.append(random.getrandbits(1))
    print("Key : ",ba2int(input_key))

    # On génère les sous clés
    W_keys, K_keys = key_scheduling(input_key)

    print("On récupère n clés W : ",len(W_keys))
    print("On récupère n clés K : ",len(K_keys))

    
    # TEST TEXTE
    data = bitarray()
    data.frombytes(b"Hello World ! Hello World ! Hello World ! Hello World !")
    print("Original: ",data.tobytes().decode("utf-8"))

    encrypted = cobra_encrypt(input_key, data)

    print(len(int2ba(encrypted)))

    input_key2 = bitarray()
    for i in range(256):
        input_key2.append(random.getrandbits(1))


    decrypted = cobra_decrypt(input_key, encrypted)
    try:
        print("Decrypted : ",get_array_from_int(decrypted).tobytes().decode("latin-1"))
    except:
        print("Error decoding")
        print("Decrypted : ",get_array_from_int(decrypted))
        



    # TEST PDF

    if (input("Voulez-vous continuer avec un fichier ? (y/n) : ") == "n"):
        exit()
    print("Chiffrement de docs/Projet_A24_coffreFort.pdf vers docs/Projet_A24_coffreFort_encrypted.pdf")
    print("...")

    data = bitarray()
    # # Ouvrir le fichier avec bitarray
    with open("docs/Projet_A24_coffreFort.pdf", "rb") as f:
        data = bitarray()
        data.fromfile(f)

    encrypted = cobra_encrypt(input_key, data)

    e = get_array_from_int(encrypted)
    with open("docs/Projet_A24_coffreFort_encrypted.bin", "wb") as f:
        e.tofile(f)

    print("Déchiffrement de docs/Projet_A24_coffreFort_encrypted.bin vers docs/Projet_A24_coffreFort_decrypted.pdf")
    print("...")

    with open("docs/Projet_A24_coffreFort_encrypted.bin", "rb") as f:
        encrypted = bitarray()
        encrypted.fromfile(f)

    decrypted = cobra_decrypt(input_key, encrypted)

    d = get_array_from_int(decrypted)
    with open("docs/Projet_A24_coffreFort_decrypted.pdf", "wb") as f:
        d.tofile(f)
    s = time.time()
    print("fin...")
    print("Temps : ",time.time()-s)


    