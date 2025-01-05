#!/usr/bin/env python3

import os, argparse
from services import *
from crypto.diffie_hellman import *
from crypto.utils import get_array_from_int, print_int_to_string, string_to_int
from crypto.rsa import *
import logging_config, logging
from services.Endpoint import establish_session, verify_ZKP

from bitarray.util import int2ba, ba2int
from bitarray import bitarray
logging_config.init_logging(False)

logger = logging.getLogger(__name__)

# Un nombre premier <= 256 bits
p = 88677346691640870283146426367756144755778293350694366754076492613699023991223
# Générateur
g = 5

client = None

def input_selection (options, message=""):
    # q une liste de choix

    if message != "":
        print(message)

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

    while password == "":
        password = input("Password >")

    client = Client(name,password)

    return establish_session(client,server,cert_auth,p,g), client
        

def create_account(name="", password=""):
    while name == "":
        name = input("Enter your username >")
    while password == "":
        password = input("Enter your password >")

    client = Client(name,password)
    if not cert_auth.create_account(name,client.generate_certificate()):
        return False
    server.create_account(name)
    return establish_session(client,server,cert_auth,p,g), client

def delete_account(name):
    server.delete_account(name)
    return cert_auth.delete_account(name)
    
def logged_in_menu():
    print("Successfully logged in !")
    while True:
        options = ["Save a file on the server", "Get a file from the server", "Log out"]

        choice = input_selection(options, "What would you like to do ?")

        if choice == 1:
            print("Save a file")
        elif choice == 2:
            print("Get a file")
        elif choice == 3:
            print("Logging out...")
            main_menu()
            break
        else:
            print("Leaving...")
            break


        choice = input_selection(options)

def get_file(filename, directory, output):
    content,_ = server.get_file(client.name, filename)

    if not content:
        print("File not found")
        return
    
    # Decrypt the file
    decrypted_file = client.rsa_decrypt_1024(content)

    # Get the number of bytes in the int decrypted_file
    size = decrypted_file.bit_length()

    # Round up to the nearest multiple of 8
    if size % 8 != 0:
        size = (size // 8 + 1) * 8

    ba = int2ba(decrypted_file, size)
    
    
    with open(directory + output, "wb") as file:
        ba.tofile(file)
    
    print(f"Server file {filename} copied to {directory}{output}")

def get_all_files(directory):
    files = server.list_files(client.name)
    for file in files:
        get_file(file, directory, file)

def save_file(filename):
    # Check if the file exists
    if not os.path.exists(filename):
        print("File does not exist")
        return
    
    # Read the file as an integer
    ba = bitarray()
    
    with open(filename, "rb") as file:
        ba.fromfile(file)

    #print(ba)

    file = ba2int(ba)

    #print(get_blocs_64bits(file))

    # Encrypt the file
    encrypted_1024_blocs = client.rsa_encrypt(file)
    


    # Send the file to the server encrypted by the Diffie-Hellman session
    #encrypted_communication = client.sessions[server.name].encrypt(encrypted_file)

    #decrypted_communication = server.sessions[client.name].decrypt(encrypted_communication)
    
    # Save the file on the server
    filename = os.path.basename(filename)
    server.save_file(client.name, filename, encrypted_1024_blocs)

    print(f"File {filename} saved on the server")

def list_files(username):
    files = server.list_files(username)
    print("Files in the server :")
    for file in files:
        print(file)

def delete_file(filename):
    return server.delete_file(client.name, filename)


def main_menu():
    print("Welcome to the server !")
    while True:
        options = ["Login","Create an account"]
        choice = input_selection(options, "What would you like to do ?")

        if choice == 1:
            if(login()):
                logged_in_menu()
                break
            else:
                print("Login failed")
        elif choice == 2:
            if(create_account()):
                logged_in_menu()
                break
            else:
                print("Account creation failed")
        else:
            print("Leaving...")
            break

if __name__ == "__main__":


    # CLI Arguments 
    parser = argparse.ArgumentParser(description="Digital safe CLI tool")
    parser.add_argument("-c", "--create", help="Create an account username:password")
    parser.add_argument("-u", "--user", help="Login username:password")
    parser.add_argument("-da" ,"--delete-account", action="store_true", help="Delete the account")
    

    parser.add_argument("-s", "--save", metavar='FILENAME', help="Save a file on the server")
    parser.add_argument("-l", "--list", action="store_true", help="List all files on the server")
    parser.add_argument('-g', '--get', metavar='FILENAME', help='Get a file from the server')
    parser.add_argument("-ga", "--get-all", action="store_true", help="Get all files from the server")
    parser.add_argument("-d", "--delete", help="Delete an account")
    parser.add_argument("-da", "--delete-all", help="Delete all files from the server")
    parser.add_argument("-o" ,"--output", help="Output name of the file to copy") 

    
    
    parser.add_argument('directory', nargs='?', help="Directory to copy (default: current directory)")

    args = parser.parse_args()

    if (args.get or args.save or args.delete or args.list or args.delete_account) and (not (args.user or args.create)):
        print("Login required before actions : get, save, delete, list")
        exit()

    if args.user and args.create:
        print("You can't login and create an account at the same time")
        exit()

    client = None
    server = Server("Server","PassWordServer")
    cert_auth = CertificationAuth("CertAuth","PassWordCertAuth")

    if not cert_auth.get_certificate("Server"):
        cert_auth.create_account("Server",server.generate_certificate())

    if not any(vars(args).values()):
        # If no arguments are passed, run the main loop menu
        main_menu()
    
    if args.create:
        try:
            create_info = args.create.split(":")
            username = create_info[0]
            password = create_info[1]
        except:
            print("Invalid username:password format")
            exit()
        success,client = create_account(username, password)
        if(success):
            print("Account created")
        else:

            print("Account creation failed")
            exit()
        
    if args.user:
        try:
            login_info= args.user.split(":")
            username = login_info[0]
            password = login_info[1]  
        except:
            print("Invalid username:password format")
            exit()
        success,client = login(username, password)
        if not success:

            print("Login failed")
            exit()

    if args.directory:
        directory = args.directory
    else:
        directory = ""

    if args.delete_account:
        if delete_account(username):
            print("Account deleted")
        else:
            print("Account deletion failed")

    elif args.list:
        list_files(username)
    elif args.get:
        if args.output:
            output = args.output
        else:
            output = args.get

        get_file(args.get, directory, output)
    elif args.all:
        get_all_files(directory)
    elif args.save:
        save_file(args.save)
    elif args.delete:
        if(delete_file(args.delete)):
            print("File deleted")
        else:
            print("File deletion failed")

    elif args.delete_all:
        delete_all_files()
        
    