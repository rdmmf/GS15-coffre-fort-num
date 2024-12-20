import crypto.diffie_hellman as diffie_hellman
from crypto.cobra import cobra_encrypt, cobra_decrypt
from bitarray import bitarray
from bitarray.util import int2ba, ba2int

class Session:
    """
    Classe des sessions partagées entre les endpoints pour s'envoyer des messages
    Les messages sont chiffrés avec le chiffrement de cobra
    La clé de session est issue de l'algorithme de Diffie-Hellman
    """

    def __init__(self, local_private_key, remote_public_key, p, g):
        self.local_private_key = local_private_key
        self.remote_public_key = remote_public_key

        self.p = p
        self.g = g

        self.shared_key = diffie_hellman.generate_shared_key(self.local_private_key, self.remote_public_key, p)

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
        
        return cobra_decrypt(shared_bitarray_key, message_bitarray)