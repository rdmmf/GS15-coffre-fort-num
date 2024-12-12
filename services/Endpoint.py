import logging, random
from .Session import Session
import crypto.diffie_hellman as diffie_hellman
from crypto.hash import hash
class Endpoint:

    """
    Classe mère de CertificationAuth, Client et Server
    Gère les communications entre les entités avec des sessions chiffrées par Cobra
    """

    def __init__(self, name, password, p, g):
        self.name = name
        self.p = p
        self.g = g

        # Dictionnaires des sessions en cours identifiées par la clé publique de l'entité distante
        self.sessions = {}

        # On utilise le mot de passe pour générer un couple de clé privée/publique
        # LE RANDOM EST TEMPORAIRE
        self.private_key = hash(password)
        self.public_key = diffie_hellman.generate_public_key(p, g, self.private_key)

        self.logger = logging.getLogger(self.name)

    def establish_session(self, remote_public_key):
        
        session = Session(self.private_key, remote_public_key, self.p, self.g)
        self.sessions[remote_public_key] = session

        return session
    

    

