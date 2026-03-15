# ✍️ AI Writing Coach

A full-stack AI Writing Coach powered by React, FastAPI, and Groq. Provides real-time, streaming text analysis and tone-specific editing suggestions (Academic, Business, Creative) in a responsive dashboard.

## 🔄 Architecture & Data Flow

Below is the real-time streaming architecture of the application:

```mermaid
sequenceDiagram
    autonumber
    participant Client as React Frontend (Vite)
    participant Server as Python FastAPI
    participant Groq as Groq API (Llama 3.1)

    Client->>Server: POST /api/analyze-text {text, mode}
    Note over Server: Injects tone-specific system prompt
    Server->>Groq: Async request to Llama 3.1-8b-instant
    Groq-->>Server: Yields data chunks (Stream=True)
    Server-->>Client: StreamingResponse (Server-Sent Events)
    Note over Client: TextDecoder renders real-time typewriter effect
