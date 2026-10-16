import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
APP_DIR = Path(__file__).parent
KNOWLEDGE_DIR = APP_DIR / "knowledge"

st.set_page_config(page_title="ChainSage AI", page_icon="⛓️", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #f6faff 0%, #ffffff 48%); }
    .hero { padding: 1.3rem 1.5rem; border-radius: 18px; color: white;
            background: linear-gradient(120deg, #102d46, #126b82); margin-bottom: 1rem; }
    .hero h1 { color: white; margin-bottom: .25rem; }
    .muted { color: #526477; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_documents():
    docs = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8").strip()
        # Simple, beginner-friendly chunking by paragraphs.
        for index, paragraph in enumerate([p.strip() for p in content.split("\n\n") if p.strip()], start=1):
            docs.append({
                "text": paragraph,
                "source": path.name,
                "chunk": index,
            })
    return docs

def retrieve(question, docs, top_k=3):
    if not docs:
        return []
    corpus = [d["text"] for d in docs]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(corpus + [question])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    ranked = scores.argsort()[::-1][:top_k]
    results = []
    for idx in ranked:
        if scores[idx] > 0:
            item = dict(docs[idx])
            item["score"] = float(scores[idx])
            results.append(item)
    return results

def generate_answer(question, sources):
    api_key = os.getenv("NEBIUS_API_KEY", "").strip()
    model = os.getenv("NEBIUS_MODEL", "").strip()
    if not api_key or not model:
        # No model call is made in demo mode. This is intentionally transparent.
        if not sources:
            return ("I couldn't find relevant information in the current knowledge base. "
                    "Try rephrasing the question or add a relevant document.")
        snippets = "\n\n".join(
            f"- {s['text']} (Source: {s['source']}, paragraph {s['chunk']})"
            for s in sources
        )
        return ("**Demo retrieval mode:** no LLM API call was made. Here are the most "
                "relevant passages found in the local knowledge base:\n\n" + snippets +
                "\n\nAdd a Nebius API key and model name in `.env` to enable generated answers.")

    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.studio.nebius.com/v1/",
        )
        context = "\n\n".join(
            f"[{s['source']} — paragraph {s['chunk']}]\n{s['text']}"
            for s in sources
        )
        if not context:
            context = "No relevant passages were retrieved."
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are ChainSage, a careful blockchain learning assistant. "
                        "Answer using only the supplied context. If the context does not "
                        "support an answer, say you do not know from the available sources. "
                        "Do not invent live transaction data, prices, or security guarantees. "
                        "Cite supporting source filenames in square brackets."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nRetrieved context:\n{context}",
                },
            ],
            temperature=0.2,
            max_tokens=600,
        )
        return response.choices[0].message.content or "The model returned an empty answer."
    except Exception as exc:
        return (
            "The Nebius API request failed, so no generated answer is available. "
            "Check your API key, model name, network connection, and account access. "
            f"\n\nTechnical detail: `{type(exc).__name__}: {exc}`"
        )

with st.sidebar:
    st.title("⛓️ ChainSage")
    st.caption("Blockchain answers grounded in a small local knowledge base.")
    st.divider()
    st.subheader("Project status")
    st.write("✅ Local document retrieval")
    st.write("✅ Source paragraph references")
    st.write("🔌 Optional Nebius model API")
    st.write("⬜ Live blockchain data (not implemented)")
    st.write("⬜ Smart-contract security analysis (not implemented)")
    st.divider()
    st.caption("Prototype only. Not financial or security advice.")

st.markdown("""
<div class="hero">
  <h1>⛓️ ChainSage AI</h1>
  <p>Ask blockchain questions. Explore the evidence. Learn with confidence.</p>
</div>
""", unsafe_allow_html=True)

docs = load_documents()
st.caption(f"Knowledge base: {len(docs)} text passages from {len(list(KNOWLEDGE_DIR.glob('*.md')))} Markdown files.")

with st.expander("Try a sample question"):
    st.write("What is the difference between Bitcoin and Ethereum?")
    st.write("What does a smart contract do?")
    st.write("What are the limitations of blockchain data?")

question = st.text_area(
    "Your blockchain question",
    placeholder="Example: What is a smart contract, and what are its limitations?",
    height=90,
)

top_k = st.slider("Number of passages to retrieve", min_value=1, max_value=5, value=3)

if st.button("Research question", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        with st.spinner("Searching the knowledge base..."):
            sources = retrieve(question.strip(), docs, top_k=top_k)
        st.subheader("Answer")
        answer = generate_answer(question.strip(), sources)
        st.markdown(answer)

        st.subheader("Retrieved evidence")
        if not sources:
            st.info("No matching passages found. The knowledge base may not cover this question yet.")
        else:
            for i, source in enumerate(sources, start=1):
                with st.expander(f"{i}. {source['source']} · paragraph {source['chunk']} · match {source['score']:.2f}"):
                    st.write(source["text"])

st.divider()
st.caption("ChainSage AI is a prototype. Retrieval relevance is approximate and answers should be independently verified.")
