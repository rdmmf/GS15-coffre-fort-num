import random
from crypto.utils import generate_prime
from crypto.hash import hash

def generate_rsa_keys(seed, bits=512, e=65537):
    p = generate_prime(bits // 2, seed)
    q = generate_prime(bits // 2, seed)
    n = p * q
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return (e, n), (d, n)

def prover_generate_certificate_Cert(e,n,secret):
    Cert = pow(secret, e, n)
    return Cert

def prover_generate_witness_M(m, e, n):
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


def guillou_quisquater_protocol():
    # Prover
    seed = hash("password")
    print(seed)
    public_key, private_key = generate_rsa_keys(seed)
    e, n = public_key
    d, _ = private_key

    print(public_key,private_key)

    # Le prover choisit un secret x et en déduit le certificat associé
    secret = random.randint(2, n - 1)
    Cert = prover_generate_certificate_Cert(e,n,secret)
    m = random.randint(2, n - 1)
    M = prover_generate_witness_M(m, e, n)

    # Il envoie Cert, e, n, M au verifieur
    
    # Le verifieur générère un défi aléatoire r 
    r = verifier_generate_challenge_r(e)

    # Le prouveur génère la preuve liée au défi r
    Proof = prover_generate_proof(n,secret,m,r)

    # Il envoie Proof au verifieur

    # Le verifieur vérifie la preuve
    verification = verifier_verify_M(Cert,r,Proof,e,n,M)

    print(verification)