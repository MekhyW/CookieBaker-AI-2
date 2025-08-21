from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    initial_processing_node,
    intent_router_node,
    general_conversation_node,
    web_search_node,
    function_call_node,
    self_awareness_node,
    tool_execution_main_bot_api_node,
    denial_message_generation_node,
    response_generation_personality_infusion_node,
    memory_update_context_storage_node,
    send_response_to_main_bot_node,
)

def build_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("initial_processing", initial_processing_node)
    workflow.add_node("intent_router", intent_router_node)
    workflow.add_node("access_control_admin_action", access_control_admin_action_node)
    workflow.add_node("general_conversation", general_conversation_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("function_call", function_call_node)
    workflow.add_node("self_awareness", self_awareness_node)
    workflow.add_node("tool_execution_main_bot_api", tool_execution_main_bot_api_node)
    workflow.add_node("denial_message_generation", denial_message_generation_node)
    workflow.add_node("response_generation_personality_infusion", response_generation_personality_infusion_node)
    workflow.add_node("memory_update_context_storage", memory_update_context_storage_node)
    workflow.add_node("send_response_to_main_bot", send_response_to_main_bot_node)
    workflow.set_entry_point("initial_processing")
    workflow.add_edge("initial_processing", "intent_router")
    workflow.add_conditional_edges(
        "intent_router",
        lambda state: state["intent"],
        {
            "admin_intent": "tool_execution_main_bot_api" if state["is_admin"] else "denial_message_generation",
            "general_conversation_intent": "general_conversation",
            "function_call_intent": "function_call",
            "self_awareness_intent": "self_awareness",
        },
    )
    workflow.add_conditional_edges(
        "general_conversation",
        lambda state: "web_search" if state["requires_web_search"] else "response_generation_personality_infusion",
        {
            "web_search": "web_search",
            "response_generation_personality_infusion": "response_generation_personality_infusion",
        },
    )
    workflow.add_edge("web_search", "response_generation_personality_infusion")
    workflow.add_edge("function_call", "memory_update_context_storage") # Assuming function call results are directly stored
    workflow.add_edge("self_awareness", "response_generation_personality_infusion")
    workflow.add_edge("tool_execution_main_bot_api", "memory_update_context_storage")
    workflow.add_edge("denial_message_generation", "response_generation_personality_infusion")
    workflow.add_edge("response_generation_personality_infusion", "memory_update_context_storage")
    workflow.add_edge("memory_update_context_storage", "send_response_to_main_bot")
    workflow.add_edge("send_response_to_main_bot", END)
    return workflow.compile()