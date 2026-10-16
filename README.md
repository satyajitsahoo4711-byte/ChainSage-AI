# ChainSage AI — starter project

A beginner-friendly blockchain Q&A prototype using Retrieval-Augmented Generation (RAG) principles.

## What works in this starter

- Streamlit web interface.
- Local retrieval from Markdown documents using TF-IDF.
- Displays source filename, paragraph number, and a rough match score.
- Optional answer generation using the OpenAI-compatible Nebius AI Studio API.
- Retrieval-only demo mode when API credentials are not configured.

## What is not implemented

- Live blockchain or explorer integration.
- Wallet connection or transaction signing.
- Smart-contract vulnerability scanning.
- Production-grade semantic embeddings/vector database.
- User accounts, authentication, or production deployment.

## Run locally

Use Python 3.10 or newer.

### Windows

1. Install Python from https://www.python.org/downloads/ and enable the option to add Python to PATH.
2. Extract this project ZIP.
3. Open Command Prompt in the extracted `chainsage_ai_starter` folder.
4. Create and activate a virtual environment:

   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```

5. Install dependencies:

   ```bat
   python -m pip install -r requirements.txt
   ```

6. Start the app:

   ```bat
   python -m streamlit run app.py
   ```

Streamlit will print a local URL (usually http://localhost:8501). Open it in your browser.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Enable Nebius AI model responses (optional)

1. Use an authorized Nebius AI Studio account and create an API key.
2. Copy `.env.example` to a file named `.env`.
3. Add your key to `NEBIUS_API_KEY`.
4. Set `NEBIUS_MODEL` to a model ID available to your account. Check the Nebius AI Studio model list/API documentation; model availability may change.
5. Restart Streamlit.

Keep `.env` private. Never commit API keys to GitHub or include them in screenshots or your Devpost submission. API usage may incur charges, so check your account's terms and limits before enabling it. If no key/model is configured, the app stays in retrieval-only demo mode.

Nebius API documentation: https://api.studio.nebius.com/docs

## Improve the prototype next

1. Test the sample questions and questions that are not covered by the documents.
2. Add more reliable, clearly attributed documentation to `knowledge/`.
3. Add evaluation examples and measure whether the correct passages are retrieved.
4. Replace TF-IDF with embeddings and a vector database if time allows.
5. Deploy only after testing, then add the real demo URL and repository to Devpost.

## Submission honesty checklist

Only claim features that you have personally run and tested. Describe Nebius-powered generation as implemented only after a successful API response. Do not claim live blockchain access or smart-contract auditing unless you build and verify those features.
