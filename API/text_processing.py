from fastapi import APIRouter, HTTPException
from models import TextRequest
from database import save_user_message
import tensorflow as tf
from transformers import BertTokenizer, TFBertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

router = APIRouter()

model_path = "saved_bert_model"
model = tf.keras.models.load_model(model_path)
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["HelpBusiness"]
collection = db["Websites"]

async def load_documents():
    documents = {}
    async for doc in collection.find():
        for hash_key, doc_data in doc["documents"].items():
            title = doc_data.get("title", "")
            raw_text = doc_data.get("raw_text", "")
            text = f"{title} {raw_text}"
            documents[hash_key] = text
    return documents

documents = {}
document_embeddings = None

def get_embeddings(texts):
    inputs = tokenizer(texts, return_tensors="tf", padding=True, truncation=True, max_length=128)
    bert_model = TFBertModel.from_pretrained("bert-base-uncased")
    outputs = bert_model(inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()

async def update_document_embeddings():
    global documents, document_embeddings
    documents = await load_documents()
    document_embeddings = get_embeddings(list(documents.values()))

asyncio.run(update_document_embeddings())

def find_relevant_documents(query, document_embeddings, documents):
    query_embedding = get_embeddings([query])
    similarities = cosine_similarity(query_embedding, document_embeddings)
    most_relevant_indices = np.argsort(similarities[0])[-4:][::-1]
    return [(list(documents.keys())[i], list(documents.values())[i]) for i in most_relevant_indices]

@router.post("/process_text")
async def process_text(request: TextRequest):
    relevant_documents = find_relevant_documents(request.text, document_embeddings, documents)
    if relevant_documents:
        await save_user_message(request.user_id, "user", request.text)
        result = " ".join([doc_text for _, doc_text in relevant_documents])
        await save_user_message(request.user_id, "bot", result)
        return {"result": result}
    raise HTTPException(status_code=500, detail="Failed to process text")
