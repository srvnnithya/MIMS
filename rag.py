from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class StoryKnowledgeBase:
    def __init__(self, persist_directory="./chroma_db"):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.persist_directory = persist_directory
        self.vectorstore = Chroma(
            collection_name="story_lore",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
        
    def add_story(self, story_text: str):
        # We simply recreate the collection to reset the lore
        try:
            self.vectorstore.delete_collection()
        except Exception:
            pass # ignore if it doesn't exist
            
        self.vectorstore = Chroma(
            collection_name="story_lore",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        # Simple chunking logic
        lines = story_text.split('\n')
        chunks = []
        current_chunk = ""
        for line in lines:
            if len(current_chunk) + len(line) > 500:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += "\n" + line
        if current_chunk:
            chunks.append(current_chunk)
            
        documents = [Document(page_content=c, metadata={"source": "story"}) for c in chunks if c.strip()]
        self.vectorstore.add_documents(documents)
        
    def retrieve_context(self, query: str, k: int = 3):
        results = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in results])
