#!/usr/bin/env python3

import os, argparse
import crypto.keys as keys

def input_selection (options):
    # q une liste de choix

    for i, choice in enumerate(options):
        print(str(i+1)+") "+ choice)
    print("q) Quit")
    
    # Vérifier la validitré de l'entrée
    while True:
        choice_input = input(">")

        if choice_input.lower() == "q" or choice_input.lower() == "quit":
            return len(options) + 1

        try:
            choice = int(choice_input)
        except:
            print("Invalid input")
            continue

        if choice < 1 or choice > len(options):
            print("Invalid input")
        else:
            return choice
        
def login(name="", password=""):
    while name == "":
        name = input("Username >")

    # Check if the account exists
    if not os.path.exists("accounts/"+name):
        print("Account not found")
        return
    
    while password == "":
        password = input("Password >")
    
    # TEMPORAIRE
    with open("accounts/"+name+"/password.txt", "r") as f:
        saved_password = f.read()

    print("Logged in" if saved_password == password else "Wrong password")

def create_account(name="", password=""):
    while name == "":
        name = input("Enter your username >")
    while password == "":
        password = input("Enter your password >")

    # if no accounts directory, create it
    if not os.path.exists("accounts"):
        os.makedirs("accounts")
    
    # Create the account directory
    if os.path.exists("accounts/"+name):
        print("Account already exists")
        return
    
    # Create the account
    try: 
        os.makedirs("accounts/"+name) 
    except:
        print("Error while creating the account")
        return
    
    # Save the password
    with open("accounts/"+name+"/password.txt", "w") as f:
        f.write(password)

    print("Account created")

def main():
    # Main menu loop
    while True:
        options = ["Login to an account", "Create an account"]
        choice = input_selection(options)

        if choice == 1:
            login()
        elif choice == 2:
            create_account()
        else:
            print("Leaving...")
            break

if __name__ == "__main__":


    # CLI Arguments 
    parser = argparse.ArgumentParser(description="Digital safe CLI tool")
   
    parser.add_argument("-l", "--login", help="Login username:password", required=False)
    parser.add_argument("-c", "--create-account", help="Login username:password", required=False)

    args = parser.parse_args()

    if args.create_account:
        try:
            log_info = args.create_account.split(":")
            create_account(log_info[0], log_info[1])
        except:
            print("Invalid username:password format")
    if args.login:
        try:
            log_info = args.login.split(":")
            login(log_info[0], log_info[1])
        except:
            print("Invalid username:password format")
    else:
        # If no arguments are passed, run the main loop
        main()

    

    