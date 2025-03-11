from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os
import time
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
from flask import Flask,render_template,url_for,request

global_embeddings = OpenAIEmbeddings()
global_loader = PyPDFLoader("artifacts/data_transformation/repo.pdf")
global_docs = global_loader.load()
global_text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
global_final_documents = global_text_splitter.split_documents(global_docs)
global_vectors = FAISS.from_documents(global_final_documents, global_embeddings)

global_llm = ChatOpenAI(model='gpt-3.5-turbo')

global_prompt = ChatPromptTemplate.from_template(
    """
you are a personal AI assistant for lokesh. 
Your provided with information of lokesh like, his project repository details, his education, his achievemets and skill set.

Answer the following question related to lokesh based only on the provided context.
Think step by step before providing a detailed answer.
I will tip you $999 if the user finds the answer helpful.
if the context is not sufficient then reply with
"I am sorry i dont have access to that data yet"

<context>
{context}
</context>
question:{input}
"""
)
global_document_chain = create_stuff_documents_chain(global_llm, global_prompt)
global_retriever = global_vectors.as_retriever(search_kwargs={"k": 30})
global_retriever_chain = create_retrieval_chain(global_retriever, global_document_chain)


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            start = time.process_time()
            # Invoke the retrieval chain with the prompt
            res = global_retriever_chain.invoke({"input": prompt})
            elapsed = time.process_time() - start
            print("Response Time:", elapsed)
            answer = res['answer']
    return render_template('index.html', answer=answer)



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)