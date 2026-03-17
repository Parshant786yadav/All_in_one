# Deploying on Render

## Start command (keep as-is)
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```
Render sets `$PORT`; the app must listen on that port.

---

## DocuMind (LLM Chatbot): OTP and Google login

### OTP (email) login
For "Send OTP" to work, set these **Environment Variables** in Render (Dashboard → your service → Environment):

| Key | Value |
|-----|--------|
| `GMAIL_OTP_EMAIL` | Your Gmail address (e.g. `you@gmail.com`) |
| `GMAIL_OTP_APP_PASSWORD` | A [Gmail App Password](https://support.google.com/accounts/answer/185833) (not your normal password) |

If these are missing, the app will return a clear error asking you to set them.

### Continue with Google
1. **Environment variables** in Render:
   - `GOOGLE_CLIENT_ID` – from Google Cloud Console → APIs & Services → Credentials → your OAuth 2.0 Client ID
   - `GOOGLE_CLIENT_SECRET` – same OAuth client’s secret

2. **Authorized redirect URI** in Google Cloud Console:
   - Open your OAuth 2.0 Client ID → **Authorized redirect URIs** → Add:
   - `https://<your-render-service-name>.onrender.com/llm-chatbot/auth/google`
   - Example: `https://all-in-one-7ds1.onrender.com/llm-chatbot/auth/google`
   - Use **https** and the exact path `/llm-chatbot/auth/google`.

The app trusts Render’s proxy headers so the redirect URI is built correctly. If Google login still fails, the redirect error page will show the exact URI the app is using so you can copy it into Google Console.

---

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
