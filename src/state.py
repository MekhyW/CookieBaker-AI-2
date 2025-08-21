from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class AgentState(TypedDict):
    user_id: int
    chat_id: int
    message_text: Optional[str]
    message_photo: Optional[str] # Base64 encoded image
    is_admin: bool
    sfw: bool
    response: Optional[str]
    tool_output: Optional[Any]
    web_search_results: Optional[str]
    denial_message: Optional[str]
    retrieved_context: Optional[List[Dict[str, Any]]]
    user_profile: Optional[Dict[str, Any]]
    group_settings: Optional[Dict[str, Any]]
    intent: Optional[str] # e.g., "admin_intent", "general_conversation_intent"
    requires_web_search: Optional[bool]
    message_embedding: Optional[List[float]]
    similar_conversations: Optional[List[Dict[str, Any]]]
    conversation_id: Optional[str]  # ID of stored conversation in Qdrant
