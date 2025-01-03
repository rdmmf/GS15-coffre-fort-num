import logging, random
from .Session import Session
import crypto.diffie_hellman as diffie_hellman
from crypto.hash import *

class Endpoint:

    """
    Classe mère de CertificationAuth, Client et Server
    Gère les communications entre les entités avec des sessions chiffrées par Cobra
    """

    def __init__(self, name, password):
        self.name = name

        # Clé privée et publique de l'entité RSA
        self.RSA_private_key = None
        self.RSA_public_key = None

        # Dictionnaires des sessions en cours identifiées par la clé publique de l'entité distante
        self.sessions = {}

        #self.public_key = hash(password)
        #self.private_key = 

        self.logger = logging.getLogger(self.name)

    def initialize_session(self,id,p,g):
        session = Session(id,p,g)
        self.sessions[id] = session

    def establish_session(self,id,remote_public_key):
        
        self.sessions[id].establish_session(remote_public_key)

        self.logger.info(f"Session established with {id}")

    def end_session(self,id):
        self.sessions.pop(id)

        self.logger.info(f"Session ended with {id}")

    

