#!/usr/bin/env python3

from services import *
from crypto.diffie_hellman import *
from crypto.utils import get_array_from_int, print_int_to_string

import logging_config, logging

logging_config.init_logging()

logger = logging.getLogger(__name__)

def establish_session(endpoint_a, endpoint_b, p, g):
    # Initialiser les paramètres de Diffie-Hellman
    endpoint_a.initialize_session(endpoint_b.name, p, g)
    endpoint_b.initialize_session(endpoint_a.name, p, g)
    
    # Etablir la session avec les clés publiques de Diffie-Hellman
    endpoint_a.establish_session(endpoint_b.name, endpoint_b.sessions[endpoint_a.name].diffie_hellman_public_key)
    endpoint_b.establish_session(endpoint_a.name, endpoint_a.sessions[endpoint_b.name].diffie_hellman_public_key)

    verificationAtoB = endpoint_a.name + " to " + endpoint_b.name + " : connection established"
    encrypted = endpoint_a.sessions[endpoint_b.name].encrypt(verificationAtoB)
    decrypted = endpoint_b.sessions[endpoint_a.name].decrypt(encrypted)

    verificationBtoA = endpoint_b.name + " to " + endpoint_a.name + " : connection established"
    encrypted = endpoint_b.sessions[endpoint_a.name].encrypt(verificationBtoA)
    decrypted = endpoint_a.sessions[endpoint_b.name].decrypt(encrypted)    

def main():

    # Un nombre premier <= 256 bits
    p = 88677346691640870283146426367756144755778293350694366754076492613699023991223
    # Générateur
    g = 5


    client = Client("Alice","PassWordAliceTestTestTesTtdzestazgdyhjqkjd")
    server = Server("Server","PassWordServer")
    
    cert_auth = CertificationAuth("CertAuth","PassWordCertAuth")

    # import os
    # file_path = "data/accounts_key/Alice.pub"
    # if os.path.exists(file_path):
    #     os.remove(file_path)

    server.create_account("Alice","public key")

    # CONNECTION CLIENT SERVEUR
    establish_session(client,server,p,g)

    # CONNECTION CERT AUTH SERVEUR
    establish_session(cert_auth,server,p,g)

    # CONNECTION CERT AUTH CLIENT
    establish_session(cert_auth,client,p,g)
    
    encrypted = server.sessions["Alice"].encrypt("test")
    decrypted = client.sessions["Server"].decrypt(encrypted) # decrypted is an int, print it as a string
    print(print_int_to_string(decrypted))
    # print("Session établie:", client.sessions["Server"].shared_key == server.sessions["Alice"].shared_key)

    # Chiffrer un msg
    

main()