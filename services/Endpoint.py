import logging, random
from .Session import Session
import crypto.diffie_hellman as diffie_hellman
from crypto.hash import *
import crypto.rsa as rsa
import os

class Endpoint:

    """
    Classe mère de CertificationAuth, Client et Server
    Gère les communications entre les entités avec des sessions chiffrées par Cobra
    """

    def __init__(self, name, password):
        self.name = name

        # Clé privée et publique de l'entité RSA
        self.public_key, self.private_key = rsa.generate_rsa_keys(custom_hash(password))

        # Dictionnaires des sessions en cours identifiées par la clé publique de l'entité distante
        self.sessions = {}

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

    def rsa_encrypt(self, message, public_key=None):
        if not public_key:
            public_key = self.public_key

        return rsa.rsa_encrypt(public_key, message)
    
    def rsa_decrypt_1024(self, message):
        return rsa.rsa_decrypt_1024(self.private_key, message)
    
    def generate_certificate(self):
        cert = rsa.prover_generate_certificate_Cert(self.public_key, self.private_key[0]) # Cert = e^d mod n
        e, n = self.public_key
        return cert, e, n
    

def establish_session(endpoint_a, endpoint_b, certification_auth, p, g, verify = False):

    endpoint_a_proving_to_b = verify_ZKP(endpoint_a, certification_auth)
    endpoint_b_proving_to_a = verify_ZKP(endpoint_b, certification_auth)

    if not endpoint_a_proving_to_b or not endpoint_b_proving_to_a:
        return False

    # Initialiser les paramètres de Diffie-Hellman
    endpoint_a.initialize_session(endpoint_b.name, p, g)
    endpoint_b.initialize_session(endpoint_a.name, p, g)
    
    # Etablir la session avec les clés publiques de Diffie-Hellman
    endpoint_a.establish_session(endpoint_b.name, endpoint_b.sessions[endpoint_a.name].diffie_hellman_public_key)
    endpoint_b.establish_session(endpoint_a.name, endpoint_a.sessions[endpoint_b.name].diffie_hellman_public_key)

    if verify:
        # Vérifier que la session est bien établie
        verificationAtoB = endpoint_a.name + " to " + endpoint_b.name + " : connection established"
        encrypted = endpoint_a.sessions[endpoint_b.name].encrypt(verificationAtoB)
        decrypted = endpoint_b.sessions[endpoint_a.name].decrypt(encrypted)

        verificationBtoA = endpoint_b.name + " to " + endpoint_a.name + " : connection established"
        encrypted = endpoint_b.sessions[endpoint_a.name].encrypt(verificationBtoA)
        decrypted = endpoint_a.sessions[endpoint_b.name].decrypt(encrypted)  
    
    return True

def verify_ZKP(endpoint_challenger, certification_auth):

    public_key = certification_auth.get_certificate(endpoint_challenger.name) # Tout le monde connait la clé publique
    
    if not public_key:
        return False
    
    private_key = endpoint_challenger.private_key # Seul le prover connait sa clé privée
    
    
    Cert,e, n = public_key   
    d, _ = private_key  

    secret = d

    # Le prover choisit un secret x et en déduit le certificat associé
    m = random.randint(2, n - 1)
    M = rsa.prover_generate_witness_M(public_key,m)

    # Il envoie Cert, e, n, M au verifieur
    # Le verifieur générère un défi aléatoire r 
    r = rsa.verifier_generate_challenge_r(e)

    # Le prouveur génère la preuve liée au défi r
    Proof = rsa.prover_generate_proof(n,secret,m,r)

    # Il envoie Proof au verifieur
    # Le verifieur vérifie la preuve
    verification = rsa.verifier_verify_M(Cert,r,Proof,e,n,M)

    return verification




