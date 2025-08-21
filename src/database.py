import os
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http import models
import uuid

class QdrantDatabase:
    def __init__(self):
        self.client = None
        self.collection_name = "cookiebot_conversations"
        self._initialize_client()
        self._ensure_collection_exists()
    
    def _initialize_client(self):
        """Initialize Qdrant client with environment variables or defaults"""
        qdrant_url = os.getenv("QDRANT_URL", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        if qdrant_api_key:
            self.client = QdrantClient(url=qdrant_url, port=qdrant_port, api_key=qdrant_api_key)
        else:
            self.client = QdrantClient(host=qdrant_url, port=qdrant_port)
    
    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE) # OpenAI embedding size
                )
        except Exception as e:
            print(f"Error ensuring collection exists: {e}")
    
    def store_conversation(self, user_id: int, chat_id: int, message_text: Optional[str], message_photo: Optional[str], embedding: List[float], metadata: Dict[str, Any] = None) -> str:
        """Store conversation data with embedding"""
        point_id = str(uuid.uuid4())
        payload = {
            "user_id": user_id,
            "chat_id": chat_id,
            "message_text": message_text,
            "message_photo": message_photo,
            "timestamp": metadata.get("timestamp") if metadata else None,
            **(metadata or {})
        }
        point = PointStruct(id=point_id, vector=embedding, payload=payload)
        try:
            self.client.upsert(collection_name=self.collection_name, points=[point])
            return point_id
        except Exception as e:
            print(f"Error storing conversation: {e}")
            return None
    
    def search_similar_conversations(self, query_embedding: List[float], chat_id: int = None, user_id: int = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar conversations"""
        search_filter = None
        if chat_id or user_id:
            conditions = []
            if chat_id:
                conditions.append(models.FieldCondition(key="chat_id", match=models.MatchValue(value=chat_id)))
            if user_id:
                conditions.append(models.FieldCondition(key="user_id", match=models.MatchValue(value=user_id)))
            search_filter = models.Filter(must=conditions)
        try:
            search_results = self.client.search(collection_name=self.collection_name, query_vector=query_embedding, query_filter=search_filter, limit=limit, with_payload=True)
            return [{"id": result.id, "score": result.score, "payload": result.payload} for result in search_results]
        except Exception as e:
            print(f"Error searching conversations: {e}")
            return []
    
    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Get user profile based on conversation history"""
        # This is a placeholder - in a real implementation, you might
        # aggregate user data from multiple conversations
        try:
            search_filter = models.Filter(
                must=[models.FieldCondition(key="user_id", match=models.MatchValue(value=user_id))]
            )
            results = self.client.scroll(collection_name=self.collection_name, scroll_filter=search_filter, limit=10, with_payload=True)
            message_count = len(results[0]) if results[0] else 0 # Basic profile aggregation
            return {
                "user_id": user_id,
                "message_count": message_count,
                "name": f"User_{user_id}",  # Placeholder
                "preferences": {}  # Placeholder
            }
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return {"user_id": user_id, "name": f"User_{user_id}"}
    
    def get_group_settings(self, chat_id: int) -> Dict[str, Any]:
        """Get group settings - placeholder implementation"""
        # This would typically come from a separate collection or database
        return {
            "chat_id": chat_id,
            "welcome_message": "Welcome to the group!",
            "sfw_mode": True,
            "admin_features_enabled": True
        }

db = QdrantDatabase()