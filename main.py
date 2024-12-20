#!/usr/bin/env python3

from services import *
from crypto.diffie_hellman import *
from crypto.utils import get_array_from_int

def main():

    # Un nombre premier <= 256 bits
    p = 88677346691640870283146426367756144755778293350694366754076492613699023991223
    # Générateur
    g = 5


    client = Client("Alice","PassWordAliceTestTestTesTtestazgdyhjqkjd",p,g)
    server = Server("Server","PassWordServer",p,g)
    
    cert_auth = CertificationAuth("CertAuth","PassWordCertAuth",p,g)

    # import os
    # file_path = "data/accounts_key/Alice.pub"
    # if os.path.exists(file_path):
    #     os.remove(file_path)

    # server.create_account("Alice",client.public_key)
    
    server.load_accounts()

    # Etablir une session entre le client et le serveur
    client.establish_session(server.public_key)
    server.establish_session(server.accounts["Alice"])

    print("Session établie:", client.sessions[server.public_key].shared_key == server.sessions[client.public_key].shared_key)

    # Chiffrer un msg
    msg = "Hello World !" * 100
    encrypted = client.sessions[server.public_key].encrypt(msg)
    decrypted = server.sessions[client.public_key].decrypt(encrypted)

    print("Message déchiffré:", get_array_from_int(decrypted).tobytes().decode("latin-1"))

main()
    