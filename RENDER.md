# Deploying on Render

## Start command (keep as-is)
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```
Render sets `$PORT`; the app must listen on that port.

## Optional: Hugging Face token
To avoid rate limits and speed up model download for the LLM Chatbot RAG, add an **Environment Variable** in Render:

- **Key:** `HF_TOKEN`  
- **Value:** your Hugging Face token from https://huggingface.co/settings/tokens  

This removes the “unauthenticated requests to the HF Hub” warning.

## If you still see “Out of memory”
- The RAG model loads on **first use** (first chat/upload that uses RAG), not at startup. If the instance has only **512 MB** RAM, that first RAG request can still hit the limit.
- **Options:**  
  - Upgrade the Render instance to **1 GB** or more, or  
  - Avoid using the RAG/embedding features on the LLM Chatbot in production on the free tier.
