import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "trial.ipynb",
    "app.py",    
    "templates/index.html",
    "templates/style.css",
    "store_index.py",
    "vectorstore/db_faiss",
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file {filename}")

    if not os.path.exists(filepath):
        with open(filepath, 'w'):
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} is already created")


