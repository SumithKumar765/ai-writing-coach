# # from fastapi import FastAPI, HTTPException
# # from fastapi.responses import StreamingResponse
# # from fastapi.middleware.cors import CORSMiddleware
# # from pydantic import BaseModel
# # from google import genai
# # from google.genai import types
# # import os
# # from dotenv import load_dotenv

# # # Load the secret API key from your .env file
# # load_dotenv()

# # app = FastAPI()

# # # Allow the React frontend to communicate with this backend securely
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["http://localhost:5173"], 
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Initialize the official Google GenAI Client
# # client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# # # Define what data we expect from the React frontend
# # class TextRequest(BaseModel):
# #     text: str
# #     mode: str = "business"

# # @app.post("/api/analyze-text")
# # async def analyze_text(request: TextRequest):
# #     if not request.text.strip():
# #         raise HTTPException(status_code=400, detail="Text is required")
        
# #     # Dynamic Configuration based on mode
# #     if request.mode == "academic":
# #         temp, persona = 0.2, "You are a strict academic writing coach."
# #     elif request.mode == "creative":
# #         temp, persona = 0.8, "You are a creative writing coach."
# #     else: # business
# #         temp, persona = 0.4, "You are a professional business writing coach."

# #     system_instruction = f"{persona} Analyze for Clarity, Style, and Grammar. Format in Markdown."

# #     # Generator function to stream chunks
# #     async def stream_generator():
# #         try:
# #             # THE FIX: Using the explicit 'models/gemini-2.0-flash' syntax
# #             # We are also upgrading you to the 2.0 model which is fully supported by the new SDK
# #             async for chunk in await client.aio.models.generate_content_stream(
# #                 model="models/gemini-2.0-flash", 
# #                 contents=request.text,
# #                 config=types.GenerateContentConfig(
# #                     system_instruction=system_instruction,
# #                     temperature=temp,
# #                 )
# #             ):
# #                 if chunk.text:
# #                     yield chunk.text
# #         except Exception as e:
# #             # Handle Quota (429) or Model (404) errors gracefully
# #             error_msg = str(e)
# #             if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
# #                 yield "⚠️ **Quota Exceeded:** Free tier limit reached. Please wait and try again, or upgrade your plan at https://ai.google.dev"
# #             elif "404" in error_msg:
# #                 yield "⚠️ **Model Error:** Model not found. Please check your API key and SDK version."
# #             else:
# #                 yield f"⚠️ **Backend Error:** {error_msg}"

# #     return StreamingResponse(stream_generator(), media_type="text/event-stream")

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="127.0.0.1", port=8000)



# #mock backend for testing frontend without hitting the actual API
# import asyncio
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import StreamingResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"], 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class TextRequest(BaseModel):
#     text: str
#     mode: str = "business"

# @app.post("/api/analyze-text")
# async def analyze_text(request: TextRequest):
#     if not request.text.strip():
#         raise HTTPException(status_code=400, detail="Text is required")
        
#     # --- MOCK DATA ---
#     # We define fake responses for all 3 categories
#     if request.mode == "academic":
#         dummy_feedback = """### 🎓 Academic Review (TEST MODE)
        
# Your text lacks formal structure and objective tone. Avoid first-person pronouns (I, me) in this context. 

# **Critique:**
# * **Clarity:** The thesis is somewhat buried.
# * **Citations:** Missing verifiable sources.

# **Suggested Rewrite:**
# > "Current research suggests a significant correlation between these variables, necessitating further peer-reviewed analysis."
# """
#     elif request.mode == "creative":
#         dummy_feedback = """### 🎨 Creative Review (TEST MODE)

# I love the underlying emotion, but the imagery could be much more vivid! "Show, don't tell."

# **Critique:**
# * **Pacing:** The sentence structure feels a bit repetitive.
# * **Vocabulary:** Try using stronger, more active verbs.

# **Suggested Rewrite:**
# > "The harsh wind tore through the shattered window panes, swallowing her words before they could even escape."
# """
#     else: # business
#         dummy_feedback = """### 💼 Business Review (TEST MODE)

# This draft is a bit too lengthy for corporate communication. Executives appreciate concise, scannable emails.

# **Critique:**
# * **Actionability:** The 'Call to Action' (CTA) is unclear.
# * **Tone:** Slightly too informal for a client-facing proposal.

# **Suggested Rewrite:**
# > "Please review the attached Q3 performance metrics and provide your final approval by Friday, EOD."
# """

#     try:
#         # Generator function to simulate the AI streaming chunk by chunk
#         async def stream_generator():
#             # We split the fake text into words to simulate the typing effect
#             words = dummy_feedback.split(" ")
#             for word in words:
#                 yield word + " "
#                 # This 0.05 second delay makes it look like it's actually generating!
#                 await asyncio.sleep(0.05) 

#         return StreamingResponse(stream_generator(), media_type="text/event-stream")
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)



#clean backend using groq api call
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import AsyncGroq

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow the React frontend to communicate with this backend securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the official Groq Async Client
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

# Define what data we expect from the React frontend
class TextRequest(BaseModel):
    text: str
    mode: str = "business"

@app.post("/api/analyze-text")
async def analyze_text(request: TextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
        
    # --- Dynamic Persona Configuration ---
    if request.mode == "academic":
        temp = 0.2
        persona = "You are a strict academic writing coach."
    elif request.mode == "creative":
        temp = 0.8
        persona = "You are a creative writing coach."
    else: # business (default)
        temp = 0.4
        persona = "You are a professional business writing coach."

    system_instruction = f"{persona} Analyze the following text focusing on Clarity, Style, and Grammar. Highlight specific sentences, explain why they need improvement, and offer rewritten alternatives. Format your response cleanly in Markdown."

    try:
        # Generator function to stream chunks asynchronously from Groq
        async def stream_generator():
            # Create the streaming request to Groq using Llama 3
            stream = await client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": request.text}
                ],
                model="llama-3.1-8b-instant", # Extremely fast model for real-time coaching
                temperature=temp,
                stream=True,
            )
            
            # Read the stream chunk by chunk
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content is not None:
                    yield content

        # Return the stream directly to the React frontend
        return StreamingResponse(stream_generator(), media_type="text/event-stream")
        
    except Exception as e:
        print(f"Error during Groq streaming: {e}")
        async def error_stream():
            yield f"⚠️ **Backend Error:** Ensure your Groq API key is correct. Details: {str(e)}"
        return StreamingResponse(error_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    # This block allows you to run it directly with 'python main.py' if needed
    uvicorn.run(app, host="127.0.0.1", port=8000)