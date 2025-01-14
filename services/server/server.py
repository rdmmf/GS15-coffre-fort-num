import logging
import os
from ..Endpoint import Endpoint
from bitarray import bitarray
from bitarray.util import int2ba, ba2int

class Server (Endpoint):

    def __init__(self, name, password):
        super().__init__(name, password)
        self.logger.info("Server initialized")

        self.path = "data/server/accounts/"


    def create_account(self, username):
        # Verifier la validité du nom d'utilisateur comme nom de fichier
        if not username.isalnum():
            self.logger.error("Invalid username")
            print("Invalid username")
            return False

        # Verifier si le compte existe déjà
        if os.path.exists(self.path + username):
            self.logger.error(f"Account {username} already exists")
            print("Account already exists")
            return False
        
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        os.makedirs(self.path + username)

        self.logger.info(f"Account {username} created")

        return True
    
    def delete_account(self, username):

        # Verifier si le compte existe déjà
        if not os.path.exists(self.path + username):
            self.logger.error(f"Account {username} does not exist")
            print(f"Account {username} does not exist")
            return False
        
        path = self.path + username
        
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))

        os.rmdir(path)

        self.logger.info(f"Account {username} deleted")

        return True
    
    def list_files(self, username):
        # Verifier si le compte existe déjà
        if not os.path.exists(self.path + username):
            self.logger.error(f"Account {username} does not exist")
            print(f"Account {username} does not exist")
            return False
        
        return os.listdir(self.path + username)
    
    def save_file(self, username, filename, content):
        # Verifier si le compte existe déjà
        if not os.path.exists(self.path + username):
            self.logger.error(f"Account {username} does not exist")
            print(f"Account {username} does not exist")
            return False

        
        with open(self.path + username + "/" + filename, "w") as file:
            for bloc1024 in content:
                file.write(str(bloc1024))
                file.write("\n")

        self.logger.info(f"File {filename} saved for account {username}")
        
        return True
    
    def get_file(self, username, filename):
        # Verifier si le compte existe déjà
        if not os.path.exists(self.path + username):
            self.logger.error(f"Account {username} does not exist")
            return False
        
        
        
        with open(self.path + username + "/" + filename, "r") as file:
            content = file.read().split("\n")

        content = [int(bloc1024) for bloc1024 in content if bloc1024 != ""]


        size = len(content)

        self.logger.info(f"File {filename} retrieved for account {username}")

        return content, size
    
    def delete_file(self, username, filename):
        # Verifier si le compte existe déjà
        if not os.path.exists(self.path + username):
            self.logger.error(f"Account {username} does not exist")
            print(f"Account {username} does not exist")
            return False
        
        os.remove(self.path + username + "/" + filename)

        self.logger.info(f"File {filename} deleted for account {username}")
        
        return True
        
        
    