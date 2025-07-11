# rag_pipeline.py

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import faiss
import torch
import json
import numpy as np

# Load embedding model
embed_model = SentenceTransformer("RAG_Model/embed_model")

# Load FAISS index
index = faiss.read_index("RAG_Model/index.faiss")

# Load RAG data
with open("RAG_Model/rag_data.json", "r", encoding="utf-8") as f:
    rag_data = json.load(f)

# Load LLM and tokenizer
tokenizer = AutoTokenizer.from_pretrained("RAG_Model/llm_tokenizer", use_fast=False)
model = AutoModelForCausalLM.from_pretrained("RAG_Model/llm_weights", torch_dtype=torch.float16)
model.eval()

def generate_answer(query: str, k: int = 3) -> str:
    # Get embedding
    query_embedding = embed_model.encode([query])

    # Search FAISS index
    D, I = index.search(np.array(query_embedding).astype("float32"), k)
    context = "\n".join([rag_data[i] if isinstance(rag_data[i], str) else rag_data[i]['text'] for i in I[0]])

    # Format prompt
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

    # Tokenize and generate
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=200)

    # Decode full output
    answer = tokenizer.decode(output[0], skip_special_tokens=True)

    # Strip the prompt from the decoded output to get only the answer text
    answer_only = answer[len(prompt):].strip()

    return answer_only

