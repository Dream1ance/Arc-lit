# !pip -q install langchain_experimental langchain_core
# !pip -q install google-generativeai
# !pip -q install google-ai-generativelanguage
# !pip -q install langchain-google-genai
# !pip install unstructured
# !pip install sentence-transformers
# !pip install Chroma
# !pip install chromadb
# !pip install langchain
# !pip install -U langchain-community
# !pip install IPython 
# !pip install langchain --upgrade
# !pip install libmagic

import textwrap
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import google.generativeai as genai
from IPython.display import display
from langchain_groq import ChatGroq
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Used to store your API key
import os
#GOOGLE_API_KEY="AIzaSyBC6RzWwzmA2ipG7NJfO3oQ1W8CDXuhoaU"
#google_api_key = os.getenv('GOOGLE_API_KEY')
#genai.configure(api_key=google_api_key)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

llm = ChatGroq(model="mixtral-8x7b-32768", api_key="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",temperature=0.2)

def get_chatbot_response(link1,link2,link3,question):
    loaders = UnstructuredURLLoader(urls=[link1,link2,link3])
    print(link1,link2,link3)
    data = loaders.load()
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=1300,
        chunk_overlap=400,
    )
    docs=text_splitter.split_documents(data)

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    db= Chroma.from_documents(docs, embedding_function).as_retriever(search_kwargs={"k":3}) #

    #qa_chain = RetrievalQA.from_chain_type(
     #   llm,
      #  retriever=db,
       # return_source_documents=True )

    template = """Immerse yourself in the provided context to answer the following question. Keep your response brief and to the point. If you're unsure, it's okay to say so without guessing. Wrap up your answer with a polite "thanks for asking!"
    Remember to base your answer solely on the provided content. Do not stray from it.
    For transparency and further exploration, Add a source  of the content that you retrieved the answers from at the end of your response.. Answer the question strictly based on the provided content; refrain from diverging.
    {context}
    Question: {question}
    /n
    Source: 'Source'
    Imaginative Answer:"""
    QA_CHAIN_PROMPT = ChatPromptTemplate.from_template(template) # Run chain
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=db,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    result = qa_chain({"query": question})

    #display(result["result"])
    return result["result"]

