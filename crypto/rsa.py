import random
from crypto.utils import generate_prime
from crypto.hash import *
from bitarray import bitarray
from bitarray.util import int2ba, ba2int
from crypto.utils import get_blocs_64bits, string_to_int, print_int_to_string,  get_blocs_1024bits

def generate_rsa_keys(seed, bits=512, e=65537):
    p = generate_prime(bits // 2, seed)
    q = generate_prime(bits // 2, seed+1)
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)


    return (e, n), (d, n)

def prover_generate_certificate_Cert(public_key,secret):
    e, n = public_key
    Cert = pow(secret, e, n)
    return Cert

def prover_generate_witness_M(public_key,m):
    cert,e, n = public_key
    M = pow(m, e, n)
    return M

def prover_generate_proof(n,secret,m,r):
    Proof = (m * pow(secret, r, n)) % n
    return Proof

def prover_generate_challenge_r(e):
    r = random.randint(0, e - 1)
    return r

def verifier_generate_challenge_r(e):
    r = random.randint(0, e - 1)
    return r

def verifier_verify_M(Cert,r,Proof,e,n,M):
    cert_r = pow(Cert, -r, n)
    proof_e = pow(Proof, e, n)
    verification = (cert_r * proof_e) % n
    return verification == M

def rsa_encrypt_int_64bits(public_key, message):
    e, n = public_key
    if message >= n:
        raise ValueError("Message must be less than modulus n.")
    return pow(message, e, n)

def rsa_decrypt_int_64bits(private_key, message):
    d, n = private_key
    
    return pow(message, d, n)

def rsa_encrypt(public_key, message):
    # On découpe message en blocs de 64 bits
    blocs = get_blocs_64bits(message)

    # On chiffre chaque bloc
    encrypted = [rsa_encrypt_int_64bits(public_key, bloc) for bloc in blocs]
    # On recompose la liste de bloc de 64 bits en un seul nombre

    return encrypted

def rsa_decrypt_1024(private_key, encrypted):
    # On déchiffre chaque bloc
    decrypted = [rsa_decrypt_int_64bits(private_key, bloc) for bloc in encrypted]

    # On recompose la liste de bloc de 64 bits en un seul nombre
    resultat = 0
    for i in range(len(encrypted)):
        resultat = (resultat << 64) | decrypted[i]
    
    return resultat


def guillou_quisquater_protocol():
    # Prover
    #seed = hash("password")
    seed = custom_hash("password")
    print(seed)
    public_key, private_key = generate_rsa_keys(seed)
    e, n = public_key
    d, _ = private_key

    print(public_key,private_key)

    # Le prover choisit un secret x et en déduit le certificat associé
    secret = random.randint(2, n - 1)
    Cert = prover_generate_certificate_Cert(public_key,secret)
    m = random.randint(2, n - 1)
    M = prover_generate_witness_M(public_key,m)

    # Il envoie Cert, e, n, M au verifieur
    
    # Le verifieur générère un défi aléatoire r 
    r = verifier_generate_challenge_r(e)

    # Le prouveur génère la preuve liée au défi r
    Proof = prover_generate_proof(n,secret,m,r)

    # Il envoie Proof au verifieur

    # Le verifieur vérifie la preuve
    verification = verifier_verify_M(Cert,r,Proof,e,n,M)

    print(verification)

def test_rsa_encrypt_decrypt():
    seed = custom_hash("password")
    public_key, private_key = generate_rsa_keys(seed)

    print(public_key,private_key)

    message = int(string_to_int("BHDEBQBD !" * 100))
    
    encrypted = rsa_encrypt(public_key, message)

    decrypted = rsa_decrypt(private_key, encrypted)

    print("DECRYPT RSA",print_int_to_string(decrypted))

def test_rsa_encrypt_decrypt_64bits():
    seed = custom_hash("password")
    public_key, private_key = generate_rsa_keys(seed)

    print(public_key,private_key)

    message = 1234567890
    
    encrypted = rsa_encrypt_int_64bits(public_key, message)

    decrypted = rsa_decrypt_int_64bits(private_key, encrypted)
    print("DECRYPT RSA",decrypted)