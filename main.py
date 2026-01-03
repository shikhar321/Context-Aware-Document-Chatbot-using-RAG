import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

from google import genai
from openai import OpenAI

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# ==================================================
# 0. Load Config
# ==================================================
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# ==================================================
# 1. Load API Keys
# ==================================================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found")

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# ==================================================
# 2. Load & Split PDF
# ==================================================
PDF_PATH = config["pdf"]["path"]

loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=config["text_splitter"]["chunk_size"],
    chunk_overlap=config["text_splitter"]["chunk_overlap"]
)

documents = text_splitter.split_documents(docs)

texts = [doc.page_content for doc in documents]
metadatas = [doc.metadata for doc in documents]

# ==================================================
# 3. Safe Batch Embedding (Gemini)
# ==================================================
def embed_texts_in_batches(client, texts):
    all_embeddings = []

    for i in range(0, len(texts), config["embedding"]["batch_size"]):
        batch = texts[i:i + config["embedding"]["batch_size"]]

        response = client.models.embed_content(
            model=config["embedding"]["model"],
            contents=batch
        )

        batch_embeddings = [e.values for e in response.embeddings]
        all_embeddings.extend(batch_embeddings)

        print(f"Embedded {len(all_embeddings)} / {len(texts)} chunks")

        time.sleep(config["embedding"]["sleep_seconds"])

    return all_embeddings

# ==================================================
# 4. Create / Load Chroma DB
# ==================================================
db = Chroma(
    collection_name=config["vector_db"]["collection_name"],
    persist_directory=config["vector_db"]["persist_directory"]
)

# ==================================================
# 5. Embed Only If Needed
# ==================================================
if db._collection.count() == 0:
    print("Creating embeddings...")

    embeddings = embed_texts_in_batches(
        client=gemini_client,
        texts=texts
    )

    db._collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=[f"doc_{i}" for i in range(len(texts))]
    )

    db.persist()
    print("Embeddings saved")

else:
    print("Embeddings already exist — skipping")

# ==================================================
# 6. Q&A Logger
# ==================================================
LOG_FILE = config["logging"]["qa_log_file"]

def log_qa(question, answer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Time     : {timestamp}\n")
        f.write(f"Question : {question}\n\n")
        f.write("Answer:\n")
        f.write(answer)
        f.write("\n")

# ==================================================
# 6.5 Conversation Memory
# ==================================================
conversation_history = []
MAX_HISTORY = config["conversation"]["max_history"]

# ==================================================
# 7. Ask Loop (RAG + Memory + OpenAI)
# ==================================================
while True:
    query = input("\nAsk a question (type 'exit' to quit): ")

    if query.lower() == "exit":
        print("Exiting...")
        break

    # ---- Embed query
    query_embedding = gemini_client.models.embed_content(
        model=config["embedding"]["model"],
        contents=[query]
    ).embeddings[0].values

    # ---- Retrieve context
    results = db.similarity_search_by_vector(
        query_embedding,
        k=config["vector_db"]["top_k"]
    )

    retrieved_context = "\n\n".join([r.page_content for r in results])

    # ---- Build history context
    history_text = ""
    for turn in conversation_history[-MAX_HISTORY:]:
        history_text += f"User: {turn['question']}\n"
        history_text += f"Assistant: {turn['answer']}\n\n"

    # ---- Final prompt
    prompt = f"""
You are a helpful AI assistant answering questions using a research paper.

Conversation history:
{history_text}

Relevant document context:
{retrieved_context}

Current question:
{query}

Answer clearly, accurately, and grounded in the document.
"""

    # ---- OpenAI generation
    response = openai_client.chat.completions.create(
        model=config["llm"]["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=config["llm"]["temperature"]
    )

    answer = response.choices[0].message.content.strip()

    print("\nAnswer:\n")
    print(answer)

    # ---- Save memory
    conversation_history.append({
        "question": query,
        "answer": answer
    })

    # ---- Log to file
    log_qa(query, answer)
