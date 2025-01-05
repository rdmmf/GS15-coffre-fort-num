import logging,os

from ..Endpoint import Endpoint

class CertificationAuth (Endpoint):

    def __init__(self, name, password):
        super().__init__(name, password)
        self.logger.info("Certification Authority initialized")

        self.path = "data/certification_auth/certificates/"

    def get_certificate(self,endpoint_name):

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if not os.path.exists(self.path + endpoint_name + ".cert"):
            self.logger.error(f"Account {endpoint_name} does not exist")
            return False
        
        with open(self.path+ endpoint_name + ".cert", "rb") as f:
            # File is a format "Cert,e,n
            public_key = f.read().decode().split(",")

            cert,e,n = int(public_key[0]), int(public_key[1]), int(public_key[2])

        return cert,e,n
    
    def create_account(self, username, public_certificate):
        # Verifier la validité du nom d'utilisateur comme nom de fichier
        if not username.isalnum():
            self.logger.error("Invalid username")
            return False

        # Verifier si le compte existe déjà
        if os.path.exists(self.path + username + ".cert"):
            self.logger.error(f"Account {username} already exists")
            print(f"Account {username} already exists")
            return False
        
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        cert,e,n = public_certificate

        with open(self.path + username + ".cert", "w") as f:
            f.write(f"{cert},{e},{n}")

        self.logger.info(f"Account {username} created")

        return True
    
    def delete_account(self, username):
        # Verifier si le compte existe déjà
        if not os.path.exists(self.path + username + ".cert"):
            self.logger.error(f"Account {username} does not exist")
            return False
        
        os.remove(self.path + username + ".cert")

        self.logger.info(f"Account {username} deleted")

        return True

