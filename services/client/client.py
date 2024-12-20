import logging

from ..Endpoint import Endpoint

class Client (Endpoint):

    def __init__(self, name, password, p, g):
        super().__init__(name, password, p, g)
        self.logger.info("Client initialisé")