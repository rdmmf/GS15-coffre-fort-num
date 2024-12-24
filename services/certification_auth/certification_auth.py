import logging

from ..Endpoint import Endpoint

class CertificationAuth (Endpoint):

    def __init__(self, name, password):
        super().__init__(name, password)
        self.logger.info("Certification Authority initialized")