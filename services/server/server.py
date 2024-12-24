import logging
import os
from ..Endpoint import Endpoint
from bitarray import bitarray
from bitarray.util import int2ba, ba2int

class Server (Endpoint):

    def __init__(self, name, password):
        super().__init__(name, password)
        self.logger.info("Server initialized")

        self.path = "data/server/account_keys/"

        self.load_accounts()

    def create_account(self, username, public_key):
        # Verifier la validité du nom d'utilisateur comme nom de fichier
        if not username.isalnum():
            self.logger.error("Invalid username")
            return False

        # Verifier si le compte existe déjà
        if os.path.exists(self.path + username + ".pub"):
            self.logger.error(f"Account {username} already exists")
            return False
        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        
        if isinstance(public_key, int):
            public_key = int2ba(public_key)

        # Enregistrer la clé publique
        with open(self.path + username + ".pub", "wb") as f:
            public_key.tofile(f)

        self.load_accounts()

        self.logger.info(f"Account {username} created")
        
    def load_accounts(self):

        self.accounts = {}
        
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        
        usernames = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        
        for username in usernames:
            key = bitarray()
            with open(self.path + username, "rb") as f:
                key.fromfile(f)

            if username[-4:] == ".pub":
                username = username[:-4]

            self.accounts[username] = ba2int(key)