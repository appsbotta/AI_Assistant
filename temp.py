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
import streamlit as st

if "vector" not in st.session_state:
    st.session_state.embeddings = OpenAIEmbeddings()
    st.session_state.loader = PyPDFLoader("artifacts/data_transformation/repo.pdf")
    st.session_state.docs = st.session_state.loader.load()
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
    st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)

# loader = PyPDFLoader("artifacts/data_transformation/repo.pdf")
# docs = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap=100)
# documents = text_splitter.split_documents(docs)
# db = FAISS.from_documents(documents=documents,embedding=OpenAIEmbeddings())
# retriever = db.as_retriever(search_kwargs={"k": 30})

llm = ChatOpenAI(model='gpt-3.5-turbo')
prompt = ChatPromptTemplate.from_template(
"""
Answer the following question based only on the provided contex.
Think step by step before providing a detailed answer.
I will tip you $999 if the user finds the answer helpful.
<context>
{context}
</context>
question:{input}
""")
document_chain = create_stuff_documents_chain(
    llm,
    prompt,
)

retriever = st.session_state.vectors.as_retriever(search_kwargs={"k": 30})
retriever_chain = create_retrieval_chain(retriever,document_chain)
prompt = st.text_input("Input your prompt")
if prompt:
    start = time.process_time()
    res = retriever_chain.invoke({"input":prompt})
    print("Response Time: " ,time.process_time()-start)
    st.write(res['answer'])