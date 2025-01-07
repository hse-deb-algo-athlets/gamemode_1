import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain.memory import ConversationBufferMemory
from langchain_core.documents.base import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.load.serializable import Serializable
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from chromadb.api import ClientAPI
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from uuid import uuid4
from typing import List
import logging
import os

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

# TODO: Implement the functions of the CustomChatBot Class. Use the knowledge and code from Session_4

class CustomChatBot: 
    """
    A class representing a chatbot that uses a ChromaDB client for document retrieval
    and the ChatOllama model for generating answers.

    This chatbot uses a retrieval-augmented generation (RAG) pipeline where it retrieves
    relevant information from a custom document database (ChromaDB) and then generates
    concise answers using a language model (ChatOllama).
    """

    def __init__(self, index_data: bool) -> None:
        """
        Initialize the CustomChatBot class by setting up the ChromaDB client for document retrieval
        and the ChatOllama language model for answer generation.
        """
        # Initialize the embedding function for document retrieval
        self.embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", cache_folder="/embedding_model")
        
        # Initialize the ChromaDB client
        self.client = self._initialize_chroma_client()
        
        # Get or create the document collection in ChromaDB
        self.vector_db = self._initialize_vector_db()

        # Process pdf, embedd data and index to ChromaDB
        
        self._index_data_to_vector_db()

        # Initialize the document retriever
        self.retriever = self.vector_db.as_retriever()

        # Initialize the large language model (LLM) from Ollama
        # TODO: ADD HERE YOUR CODE
        self.llm = ChatOllama(model="llama3.2", base_url="http://ollama:11434")

        # Set up the retrieval-augmented generation (RAG) pipeline
        self.qa_rag_chain = self._initialize_qa_rag_chain()



    def _initialize_chroma_client(self) -> ClientAPI:
        """
        Initialize and return a ChromaDB HTTP client for document retrieval.

        Returns:
            chromadb.HttpClient: A client used to communicate with ChromaDB.
        """
        logger.info("Initialize chroma db client.")


        # TODO: ADD HERE YOUR CODE
        client = chromadb.HttpClient(
            host="chroma",
            port=8000,
            ssl=False,
            headers=None,
            settings=Settings(allow_reset=True, anonymized_telemetry=False),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE,
        )
        return client

    def clean_text_for_chroma(self,text: str):
    
        # 1. Entferne Unicode-Surrogatpaare
        text = re.sub(r'[\ud800-\udfff]', '', text)
    
        # 2. Entferne nicht-ASCII-Zeichen (optional, abhängig von deinem Anwendungsfall)
        # text = re.sub(r'[^\x00-\x7F]+', '', text)  # Entkommentiere dies, wenn nicht-ASCII-Zeichen entfernt werden sollen.
        
        # 3. Entferne HTML-Tags, falls der Text HTML enthält
        text = re.sub(r'<.*?>', '', text)
        
        # 4. Entferne zusätzliche Leerzeichen und Zeilenumbrüche
        text = re.sub(r'\s+', ' ', text)  # Ersetzt mehrere Leerzeichen, Tabulatoren oder Zeilenumbrüche durch ein einzelnes Leerzeichen.
        
        # 5. Entferne führende und abschließende Leerzeichen
        text = text.strip()
    
        return text

    def _initialize_vector_db(self) -> Chroma:
        """
        Initialize and return a Chroma vector database using the HTTP client.

        Returns:
            Chroma: A vector database instance connected to the document collection in ChromaDB.
        """
        logger.info("Initialize chroma vector db.")

        # TODO: ADD HERE YOUR CODE
        #self.client.delete_collection("collection_name")
        from main import momentante_pdf

        mo_collection = self.clean_text_for_chroma(momentante_pdf)
        collection = self.client.get_or_create_collection(mo_collection)
        
        vector_db_from_client = Chroma(
            client=self.client,
            collection_name=mo_collection,
            embedding_function=self.embedding_function,
        )
        
                
        for doc in collection.get()["documents"] or []:
            logger.info(doc)
        return vector_db_from_client
    
    def clean_text(self, chunk):
        text = chunk.page_content
    # Remove surrogate pairs
        text = re.sub(r'[\ud800-\udfff]', '', text)
    # Optionally remove non-ASCII characters (depends on your use case)
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        return Document(page_content=text, metadata=chunk.metadata)

    def _index_data_to_vector_db(self):
        from main import momentante_pdf
        # TODO: ADD HERE YOUR CODE
        mo_collection = self.clean_text_for_chroma(momentante_pdf)
        collection = self.client.get_or_create_collection(mo_collection)
        docs = collection.get()["documents"] or []
        if docs == []:
            logger.info("Lade Doc in vectordb")

            pdf_doc = "pdf/"+momentante_pdf
            logger.info("Aktueller Pfad: "+pdf_doc)
            loader = PyPDFLoader(file_path=pdf_doc)

            pages = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 20)
            pages_chunked = splitter.split_documents(pages)
            pages_chunked_cleaned = [self.clean_text(chunk) for chunk in pages_chunked]
            uuids = [str(uuid4()) for _ in range(len(pages_chunked_cleaned))]
            self.vector_db.add_documents(documents=pages_chunked_cleaned, id=uuids)
        



    def _initialize_qa_rag_chain(self) -> RunnableSerializable:
        """
        Set up the retrieval-augmented generation (RAG) pipeline for answering questions.
        
        The pipeline consists of:
        - Retrieving relevant documents from ChromaDB.
        - Formatting the retrieved documents for input into the language model (LLM).
        - Using the LLM to generate concise answers.
        
        Returns:
            dict: The RAG pipeline configuration.
        """

        # TODO: ADD HERE YOUR CODE
        prompt_template = """
            Du bist ein interaktiver Assistent, der in der Lage ist, sinnvolle Fragen zu einem gegebenen Kontext zu stellen.
            Ablauf:
            1.	Kontextfestlegung: Der Nutzer stellt dir einen Kontext zur Verfügung. Dieser kann ein bestimmtes Thema, ein Fachgebiet, eine Geschichte oder jede andere Art von Information sein.
            2.	Fragegenerierung: Sobald der Nutzer den Text "Stelle mir eine Frage" eingibt, generierst du eine relevante Frage, die sich auf den angegebenen Kontext bezieht. Die Frage sollte logisch aus dem Kontext folgen und den Nutzer zum Nachdenken anregen.
            3.	Antwort des Nutzers: Der Nutzer antwortet auf deine Frage mit dem Präfix "Antwort:".
            4.	Bewertung der Antwort: Du analysierst die Antwort des Nutzers und gibst eine Bewertung ab. 
            Richtig: Wenn die Antwort korrekt ist oder logisch aus dem Kontext folgt, gibst du als aller erstes "RICHTIG" aus.
            Falsch: Wenn die Antwort falsch ist oder nicht zum Kontext passt, gibst du als Antwort "Leider Falsch" aus und die Erklärung warum diese falsch ist.
            Unklar: Wenn die Antwort schwer zu bewerten ist oder weitere Informationen benötigt, kannst du eine Rückfrage stellen oder eine neutralere Bewertung abgeben.
            


            <context>
            {context}
            </context>

            {question}"""

        rag_prompt = ChatPromptTemplate.from_template(prompt_template)

        retriever = self.vector_db.as_retriever(search_kwargs={"k": 5})

        qa_rag_chain = ({"context": retriever | self._format_docs, "question": RunnablePassthrough()}
                        | rag_prompt
                        | self.llm
                        | StrOutputParser()
        )

        return qa_rag_chain


        

    def _format_docs(self, docs: List[Document]) -> str:
        """
        Helper function to format the retrieved documents into a single string.
        
        Args:
            docs (List[Document]): A list of documents retrieved by ChromaDB.

        Returns:
            str: A string containing the concatenated content of all retrieved documents.
        """

        # TODO: ADD HERE YOUR CODE
        for i, doc in enumerate(docs):
            logger.info(f"Dokument {i+1}: {doc.page_content}, Metadaten: {doc.metadata}")
            
        return "\n\n".join(doc.page_content for doc in docs)



    async def astream(self, question: str):
        """
        Handle a user query asynchronously by running the question through the RAG pipeline and stream the answer.

        Args:
            question (str): The user's question as a string.

        Yields:
            str: The generated answer from the model, streamed chunk by chunk.
        """
        logger.info("Streaming RAG chain response.")
        try:
            async for chunk in self.qa_rag_chain.astream(question): # type: ignore
                logger.debug(f"Yielding chunk: {chunk}")
                yield chunk
        except Exception as e:
            logger.error(f"Error in stream_answer: {e}", exc_info=True)
            raise