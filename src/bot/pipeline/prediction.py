from langchain_community.document_loaders import PyPDFDirectoryLoader
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

class PredictionPipeline:
    def __init__(self):
        pass

    def chain(self):
        embeddings = OpenAIEmbeddings()
        loader = PyPDFDirectoryLoader("artifacts/data_transformation")
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        final_documents = text_splitter.split_documents(docs)
        vectors = FAISS.from_documents(final_documents, embeddings)

        llm = ChatOpenAI(model='gpt-3.5-turbo',api_key=os.getenv("OPENAI_API_KEY"))

        prompt = ChatPromptTemplate.from_template(
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
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vectors.as_retriever(search_kwargs={"k": 30})
        retriever_chain = create_retrieval_chain(retriever, document_chain)
        return retriever_chain

