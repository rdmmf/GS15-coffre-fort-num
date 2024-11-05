#!/usr/bin/env python3

def input_handler (options):
    # q une liste de choix

    for i, choice in enumerate(options):
        print(str(i+1)+") "+ choice)
    print("q ou quit pour quitter")
    
    
    # Vérifier la validitré de l'entrée
    while True:
        choice_input = input(">")

        if choice_input.lower() == "q" or choice_input.lower() == "quit":
            return len(options) + 1

        try:
            choice = int(choice_input)
        except:
            print("Entrée invalide")
            continue

        if choice < 1 or choice > len(options):
            print("Option invalide")
        else:
            return choice
        

def chiffrer():
    print("Chiffrer un message")

def dechiffrer():
    print("Déchiffrer un message")

if __name__ == "__main__":

    while True:
        options = ["Chiffrer un message", "Déchiffrer un message"]
        choice = input_handler(options)

        if choice == 1:
            chiffrer()
        elif choice == 2:
            dechiffrer()
        else:
            print("Quitter...")
            break