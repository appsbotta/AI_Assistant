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
from bot.constants import CONFIG_PATH
from bot.utils.common import read_yaml
import time
from dotenv import load_dotenv
load_dotenv()



class PredictionPipeline:
    def __init__(self,config_path=CONFIG_PATH):
        self.config =  read_yaml(config_path)

    def chain(self):
        embeddings = OpenAIEmbeddings()
        loader = PyPDFDirectoryLoader(self.config.prediction.folder_dir)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        final_documents = text_splitter.split_documents(docs)
        vectors = FAISS.from_documents(final_documents, embeddings)

        llm = ChatOpenAI(model='gpt-3.5-turbo',api_key=os.getenv("OPENAI_API_KEY"))

        prompt = prompt = ChatPromptTemplate.from_template(
            """
            You are Lokesh's personal AI assistant. You have been provided with a context that includes detailed information about Lokesh’s projects (project names, project URLs, updated_at, created_at, and pushed_at timestamps) as well as his personal details such as education, skills, and work experience.

            When a user asks a question related to Lokesh—whether it's about his projects, education, skills, or work experience—follow these guidelines:

            Use Only Provided Information:
            Answer strictly based on the context provided. Do not assume or add any external information.

            Detail and Accuracy:
            Extract and present accurate details from the context. For projects, include names, URLs, and date details as available.

            Step-by-Step Reasoning (if needed):
            If the question requires it, explain your reasoning by referring to the specific fields in the context.

            Insufficient Data Response:
            If the context does not have enough information to answer the question, reply exactly with:
            "Sorry, I don't have access to that data yet."

            Now, answer the user's question based solely on the provided context.

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

