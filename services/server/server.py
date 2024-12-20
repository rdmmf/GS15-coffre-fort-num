import logging
import os
from ..Endpoint import Endpoint
from bitarray import bitarray
from bitarray.util import int2ba, ba2int

class Server (Endpoint):

    def __init__(self, name, password, p, g):
        super().__init__(name, password, p, g)
        self.logger.info("Server initialized")

    def create_account(self, username, public_key):
        # Verifier la validité du nom d'utilisateur comme nom de fichier
        if not username.isalnum():
            self.logger.error("Invalid username")
            return False
        


        # Verifier si le compte existe déjà
        if os.path.exists("data/accounts_key/" + username + ".pub"):
            self.logger.error(f"Account {username} already exists")
            return False
        
        if not os.path.exists("data/accounts_key"):
            os.mkdir("data/accounts_key")
        
        if isinstance(public_key, bitarray):
            public_key = ba2int(public_key)

        # Enregistrer la clé publique
        with open("data/accounts_key/" + username + ".pub", "w") as f:
            f.write(public_key.hex())
        