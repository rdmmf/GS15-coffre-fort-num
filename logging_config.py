import logging

# Si le dossier log n'existe pas
import os
if not os.path.exists("./logs"):
    os.makedirs("./logs")

def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)-10s - %(message)s",
        handlers=[
            logging.StreamHandler(),                # Logs pour la console
            logging.FileHandler("./logs/debug.log") # Logs dans un fichier
        ]
    )