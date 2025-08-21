# CookieBaker-AI 2

Langgraph agent application for the Cookiebot project, designed to enhance their conversational abilities, integrate memory and internet search, enable natural language configuration for chat admins, and foster a unique, self-aware personality.

```mermaid
flowchart TD
 subgraph subGraph0["External Services"]
        L["Main Cookiebot Application"]
        M["MongoDB Backend"]
        N["Vector Database"]
        O["Embedding Model"]
        P["Web Search API"]
  end
    A["Received Message from Main Bot"] --> B{"Initial Processing & Context Retrieval"}
    B --> C{"Intent Router"}
    C -- Admin Intent --> D["Access Control & Admin Action"]
    C -- General Conversation Intent --> E["General Conversation Node"]
    C -- Function Call Intent --> F["Function Call Node"]
    C -- "Self-Awareness Intent" --> G["Self-Awareness Node"]
    D -- Authorized --> D1["Tool Execution: Main Bot API"]
    D -- Unauthorized --> D2["Denial Message Generation"]
    E --> E1a{"Requires Web Search?"}
    E1a -- Yes --> E1b["Web Search Node"]
    E1a -- No --> H["Response Generation & Personality Infusion"]
    E1b --> H
    D1 --> I["Memory Update & Context Storage"]
    D2 --> H
    F --> I
    G --> I
    H --> I
    I --> J["Send Response to Main Bot"]
    J --> K["End Cycle"]
    D1 -.-> L
    D -.-> L
    B -.-> M & N
    I -.-> M & N
    E1b -.-> P
```