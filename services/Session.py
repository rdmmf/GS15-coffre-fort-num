import crypto.diffie_hellman as diffie_hellman
from crypto.cobra import cobra_encrypt, cobra_decrypt
from bitarray import bitarray
from bitarray.util import int2ba, ba2int
import random
import logging
from crypto.utils import get_array_from_int

class Session:
    """
    Classe des sessions partagées entre les endpoints pour s'envoyer des messages
    Les messages sont chiffrés avec le chiffrement de cobra
    La clé de session est issue de l'algorithme de Diffie-Hellman
    """

    def __init__(self, id, p, g):

        self.p = p
        self.g = g
        self.id = id

        self.diffie_hellman_private_key = random.getrandbits(256)
        self.diffie_hellman_public_key = diffie_hellman.generate_public_key(self.p, self.g, self.diffie_hellman_private_key)

        self.shared_key = None

        self.logger = logging.getLogger(self.id)

    def establish_session(self, remote_public_key):

        self.shared_key = diffie_hellman.generate_shared_key(self.diffie_hellman_private_key, remote_public_key, self.p)

    def encrypt(self, message):
        # On vérifie le type du message
        if isinstance(message, str):
            message_bitarray = bitarray()
            message_bitarray.frombytes(message.encode("utf-8"))
        elif isinstance(message, int):
            message_bitarray = int2ba(message)
        elif isinstance(message, bitarray):
            message_bitarray = message
        else:
            raise ValueError("Message format not supported")

        shared_bitarray_key = int2ba(self.shared_key)
        
        return cobra_encrypt(shared_bitarray_key, message_bitarray)
    
    def decrypt(self, message):
        # On vérifie le type du message
        if isinstance(message, str):
            message_bitarray = bitarray()
            message_bitarray.frombytes(message.encode("utf-8"))
        elif isinstance(message, int):
            message_bitarray = int2ba(message)
        elif isinstance(message, bitarray):
            message_bitarray = message
        else:
            raise ValueError("Message format not supported")
        
        shared_bitarray_key = int2ba(self.shared_key)

        decrypted = cobra_decrypt(shared_bitarray_key, message)
        try:
            self.logger.info(f"Decoded message : " + get_array_from_int(decrypted).tobytes().decode("latin-1"))
        except Exception as e:
            self.logger.error("Decoded message but couldn't encode : " + str(e))

        return decrypted