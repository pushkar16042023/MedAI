from flask import Flask,render_template,jsonify,request
from src.helper import *
from src.prompt import *
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os
load_dotenv()

DB_FAISS_PATH = 'vectorstore/db_faiss'
data_dir = os.path.join(os.path.dirname(__file__), 'data_dir')

app = Flask(__name__)
extdata = pdf_load(data_dir)
tokens = split(extdata)
embeddings = hf_embeddings()

db = store_embeddings(tokens,embeddings)


prompt = PromptTemplate(input_variables=["context","question"],template=prompt_template)

chain_type_kwargs = {"prompt": prompt}

llm=CTransformers(model="llm/llama-2-7b-chat.ggmlv3.q4_0.bin",model_type="llama",config={'max_new_tokens':512,'temperature':0.8})
qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=db.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs)
@app.route("/")

def index():
    return render_template('index.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result = qa({"query": input})
    print("Response : ", result["result"])
    return jsonify({"response": result["result"]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)

