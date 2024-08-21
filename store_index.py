from src.helper import pdf_load,split, hf_embeddings,embed_and_store_chunks
import numpy as np
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os




DB_FAISS_PATH = 'vectorstore/db_faiss'

extdata = pdf_load("data_dir")
tokens = split(extdata)
embeddings = hf_embeddings()
embed_and_store_chunks(tokens, embeddings, DB_FAISS_PATH)


db = FAISS.from_documents(tokens, embeddings)
db.save_local(DB_FAISS_PATH)