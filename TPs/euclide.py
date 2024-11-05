#!/usr/bin/env python3

a = 123
b = 37

def PGCD(a,b):
    diviseur = b
    dividende = a

    reste = dividende % diviseur

    while reste != 0:
        dividende = diviseur
        diviseur = reste
        reste = dividende % diviseur

    return diviseur


# MARCHE PAS
def EuclideEtendu(a,b):

    u0 = 1
    u1 = 0
    v0 = 0
    v1 = 1

    diviseur = b
    dividende = a

    reste = dividende % diviseur
    quo = dividende // diviseur

    k = 0
    while reste != 0:

        dividende = diviseur
        diviseur = reste
        reste = dividende % diviseur

        quo = dividende // diviseur

        tmp = quo * u1 + u0
        u0 = u1
        u1 = tmp
        tmp = quo * v1 + v0
        v0 = v1
        v1 = tmp


        k += 1
    k+=1
    u = (-1)**k * u1
    v = (-1)**k * v1

    print("ax+by=PGCD : ", a, "*", u, "+", b, "*", v, "=", PGCD(a,b))
    return diviseur, u, v

print("PGCD de", a, "et", b, ":", PGCD(a,b))
print("Euclide étendu de", a, "et", b, ":", EuclideEtendu(a,b))
