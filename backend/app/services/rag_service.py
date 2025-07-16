from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.conversation import RagDocument
from ..schemas.conversation import RagDocumentCreate, RagDocumentResponse

class RagService:
    """Service for handling RAG (Retrieval-Augmented Generation) operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_document(self, document_data: RagDocumentCreate) -> RagDocument:
        """Create a new RAG document"""
        db_document = RagDocument(
            chatbot_id=document_data.chatbot_id,
            filename=document_data.filename,
            content=document_data.content,
            metadata=document_data.metadata
        )
        
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        
        return db_document
    
    def get_documents_by_chatbot(self, chatbot_id: int) -> List[RagDocument]:
        """Get all documents for a chatbot"""
        return self.db.query(RagDocument).filter(
            RagDocument.chatbot_id == chatbot_id
        ).all()
    
    def get_document(self, document_id: int) -> Optional[RagDocument]:
        """Get document by ID"""
        return self.db.query(RagDocument).filter(RagDocument.id == document_id).first()
    
    def delete_document(self, document_id: int) -> bool:
        """Delete a document"""
        document = self.get_document(document_id)
        if not document:
            return False
        
        self.db.delete(document)
        self.db.commit()
        return True
    
    def search_documents(self, chatbot_id: int, query: str) -> List[RagDocument]:
        """Search documents by content (basic text search)"""
        return self.db.query(RagDocument).filter(
            RagDocument.chatbot_id == chatbot_id,
            RagDocument.content.ilike(f"%{query}%")
        ).all()
    
    def process_file_upload(self, chatbot_id: int, filename: str, content: str) -> RagDocument:
        """Process uploaded file and create RAG document"""
        # Basic file processing - in production, this would include:
        # - File type validation
        # - Text extraction from various formats
        # - Content chunking
        # - Embedding generation
        
        document_data = RagDocumentCreate(
            chatbot_id=chatbot_id,
            filename=filename,
            content=content,
            metadata={"file_type": filename.split('.')[-1] if '.' in filename else "txt"}
        )
        
        return self.create_document(document_data)
    
    def get_relevant_context(self, chatbot_id: int, query: str, max_results: int = 3) -> str:
        """Get relevant context for a query (basic implementation)"""
        # This is a basic implementation - in production, this would use:
        # - Vector embeddings
        # - Semantic search
        # - Re-ranking algorithms
        
        relevant_docs = self.search_documents(chatbot_id, query)[:max_results]
        
        if not relevant_docs:
            return ""
        
        context_parts = []
        for doc in relevant_docs:
            context_parts.append(f"From {doc.filename}: {doc.content[:500]}...")
        
        return "\n\n".join(context_parts)