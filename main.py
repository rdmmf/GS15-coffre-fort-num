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

# iterations = 32
iterations = 1

def input_selection (options, message=""):
    # q une liste de choix
    print("----------------------------")
    print("    GS15 - Digital Safe ")
    print("----------------------------")
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
        return False,False
    server.create_account(name)
    return establish_session(client,server,cert_auth,p,g), client

def delete_account(name):
    server.delete_account(name)
    return cert_auth.delete_account(name)
    
def logged_in_menu(client):
    print("Successfully logged in !")
    while True:
        options = ["List files on the server","Save a file on the server", "Delete a file on the server", "Get a file from the server", "Get all files from the server", "Delete account", "Log out"]

        choice = input_selection(options, "What would you like to do ?")

        if choice == 1:
            list_files(client.name)
        elif choice == 2:
            save_file(client)
        elif choice == 3:
            delete_file(client)
        elif choice == 4:
            get_file(client)
        elif choice == 5:
            get_all_files(client)
        elif choice == 6:
            if(delete_account(client.name)):
                print("Account deleted")
                client = None
                
                main_menu()
                break
            else:
                print("Account deletion failed")
        elif choice == 7:
            print("Logging out...")
            client = None
            main_menu()
            break
        else:
            print("Leaving...")
            break

def get_file(client,filename=None, directory=None, output=None):

    if filename == None:
        filename = input("Enter the file to get >")
    if directory == None:
        directory = input("Enter the directory to save the file >")
    if output == None:
        output = filename

    encrypted_rsa_1024_blocs,_ = server.get_file(client.name, filename)

    if not encrypted_rsa_1024_blocs:
        print("File not found")
        return
    

    encrypted_cobra_1024_blocs = [client.sessions[server.name].encrypt(encrypted_rsa_1024_blocs[i],iterations) for i in range(0, len(encrypted_rsa_1024_blocs))]

    decrypted_cobra_1024_blocs = [server.sessions[client.name].decrypt(encrypted_cobra_1024_blocs[i],iterations) for i in range(0, len(encrypted_cobra_1024_blocs))]
    
    # Decrypt the file
    decrypted_file = client.rsa_decrypt_1024(decrypted_cobra_1024_blocs)



    # Get the number of bytes in the int decrypted_file
    size = decrypted_file.bit_length()

    # Round up to the nearest multiple of 8
    if size % 8 != 0:
        size = (size // 8 + 1) * 8

    ba = int2ba(decrypted_file, size)
    
    
    with open(directory + output, "wb") as file:
        ba.tofile(file)
    
    print(f"Server file {filename} copied to {directory}/{output}")

def get_all_files(client,directory=None):
    if directory == None:
        directory = input("Enter the directory to save the files >")

    files = server.list_files(client.name)
    for file in files:
        get_file(client,file, directory, file)

def save_file(client,filename=None):
    if filename == None:
        filename = input("Enter the path of the file to save >")

    # Check if the file exists
    if not os.path.exists(filename):
        print("File does not exist")
        return
    
    # Read the file as an integer
    ba = bitarray()
    
    with open(filename, "rb") as file:
        ba.fromfile(file)

    file = ba2int(ba)

    # Encrypt the file
    encrypted_1024_blocs = client.rsa_encrypt(file)

    encrypted_cobra_1024_blocs = [client.sessions[server.name].encrypt(encrypted_1024_blocs[i],iterations) for i in range(0, len(encrypted_1024_blocs))]

    decrypted_cobra_1024_blocs = [server.sessions[client.name].decrypt(encrypted_cobra_1024_blocs[i],iterations) for i in range(0, len(encrypted_cobra_1024_blocs))]
    
    # Save the file on the server
    filename = os.path.basename(filename)
    server.save_file(client.name, filename, decrypted_cobra_1024_blocs)

    print(f"File {filename} saved on the server")

def list_files(username):
    files = server.list_files(username)
    print("Files in the server :")
    for file in files:
        print(file)

def delete_file(client,filename=None):
    if filename == None:
        filename = input("Enter the file to delete >")

    return server.delete_file(client.name, filename)

def delete_all_files(client):
    files = server.list_files(client.name)
    for file in files:
        if(delete_file(client,file)):
            print(f"File {file} deleted")
        else:
            print(f"File {file} deletion failed")

def main_menu():
    print("Welcome to the server !")
    while True:
        options = ["Login","Create an account"]
        choice = input_selection(options, "What would you like to do ?")

        if choice == 1:
            success,client = login()
            if(success):
                logged_in_menu(client)
                break
            else:
                print("Login failed")
        elif choice == 2:
            success,client = create_account()
            if(success):
                logged_in_menu(client)
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
    parser.add_argument("-du" ,"--delete-user", help="Delete the account username:password")
    
    parser.add_argument("-s", "--save", metavar='FILENAME', help="Save a file on the server")
    parser.add_argument("-l", "--list", action="store_true", help="List all files on the server")
    parser.add_argument('-g', '--get', metavar='FILENAME', help='Get a file from the server')
    parser.add_argument("-ga", "--get-all", action="store_true", help="Get all files from the server")
    parser.add_argument("-d", "--delete", help="Delete a file")
    parser.add_argument("-da", "--delete-all", action="store_true", help="Delete all files from the server")
    parser.add_argument("-o" ,"--output", help="Output name of the file to copy") 

    parser.add_argument('directory', nargs='?', help="Directory to copy (default: current directory)")

    args = parser.parse_args()

    if (args.get or args.save or args.delete or args.list or args.delete_all or args.get_all) and (not (args.user or args.create)):
        print("Login required before actions : get, save, delete, list")
        exit()

    if args.user and args.create and args.delete_user:
        print("You can't login/create/delete an account at the same time")
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
    
    if args.delete_user:
        try:
            delete_info = args.delete_user.split(":")
            username = delete_info[0]
            password = delete_info[1]
        except:
            print("Invalid username format")
        success,client = login(username, password)
        if not success:

            print("Authentification failed")
        if delete_account(username):
            print("Account deleted")
            
        else:
            print("Account deletion failed")
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

    if args.list:
        list_files(username)
    elif args.get:
        if args.output:
            output = args.output
        else:
            output = args.get
        
        get_file(client,args.get, directory, output)
        
    elif args.get_all:
        get_all_files(client,directory)

    elif args.save:
        save_file(client,args.save)
    
    elif args.delete_all:
        delete_all_files(client)
    elif args.delete:
        if(delete_file(client,args.delete)):
            print("File deleted")
        else:
            print("File deletion failed")
        
        
    