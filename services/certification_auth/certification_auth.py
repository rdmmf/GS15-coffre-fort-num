import logging

class CertificationAuth:

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(self.__class__.__name__)

        self.log("Created")

    def log(self, msg):
        self.logger.info(f"[CertificationAuth {self.name}] {msg}")