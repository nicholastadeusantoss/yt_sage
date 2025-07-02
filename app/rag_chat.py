from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.schema import Document

def create_qa_chain(transcript_text: str):
    doc = Document(page_content=transcript_text)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents([doc], embeddings)
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
