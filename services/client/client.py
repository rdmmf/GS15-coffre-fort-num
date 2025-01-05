import logging, os

from ..Endpoint import Endpoint

class Client (Endpoint):

    def __init__(self, name, password):
        super().__init__(name, password)
        self.logger.info("Client initialized")