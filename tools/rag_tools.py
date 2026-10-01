from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from langchain_classic.retrievers import BM25Retriever,EnsembleRetriever
from langchain_qdrant import QdrantVectorStore 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_cohere import CohereRerank
from config import *
from langchain_groq import ChatGroq

def chunk_load(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    return chunks


def store(chunks):

    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore=QdrantVectorStore.from_documents(chunks,embeddings,url=QDRANT_URL,api_key=QDRANT_API_KEY,collection_name=COLLECTION_NAME)


    return vectorstore





def sementic_retrieval():

    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


    vectorstore=QdrantVectorStore.from_existing_collection(embedding=embeddings,url=QDRANT_URL,api_key=QDRANT_API_KEY,collection_name=COLLECTION_NAME)

    sementic=vectorstore.as_retriever(search_kwargs={"k":10})

    return sementic 


def bm25_retrieval(chunks):

    bm25=BM25Retriever.from_documents(chunks)
    bm25.k=10
    return bm25 


def hybrid_search(question,bm25,sementic,chunks):

    hybrid_retriever=EnsembleRetriever(retrievers=[bm25,sementic],weights=[0.5,0.5])

    return hybrid_retriever.invoke(question)



def cohere_reranker(hybrid_results,question):

    reranker=CohereRerank(model="rerank-english-v3.0",top_n=5,cohere_api_key=COHERE_API_KEY)

    reranked=reranker.compress_documents(hybrid_results,question)

    return reranked 


def generate_answer(reranked, question):
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY)
    context = "\n\n".join([
        (doc if isinstance(doc, str) else doc.page_content)[:1000] 
        for doc in reranked
    ])
    prompt = f"""Answer the following question based on the context below:

Context:
{context}

Question: {question}"""
    
    answer = llm.invoke(prompt)
    return answer.content







    




