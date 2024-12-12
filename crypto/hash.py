# FONCTION TEMPORAIRE

import hashlib

def hash(data):
    # Fonction hash
    hashed  =int(hashlib.sha256(data.encode()).hexdigest(), 16)

    return hashed
