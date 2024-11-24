import json
from aiohttp import ClientSession
from fastapi import APIRouter, HTTPException
from api.models import TextRequest
from api.database import get_business_by_id
import tensorflow as tf
from transformers import BertTokenizer, TFBertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

# Инициализация модели и токенизатора
model_path = "saved_bert_model"
model = tf.keras.models.load_model(model_path)
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Подключение к базе данных
client = AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["HelpBusiness"]
collection = db["Websites"]

documents = {}
document_embeddings = None

def assemble_text(data_string):
    lines = data_string.strip().splitlines()
    content = []
    for line in lines:
        if line.startswith("data: "):
            json_str = line[6:]
            try:
                json_data = json.loads(json_str)
                delta_content = json_data['choices'][0]['delta'].get('content', '')
                content.append(delta_content)
            except (json.JSONDecodeError, KeyError):
                continue
    return ''.join(content)

async def get_answer_jasper(text, user_id):
    async with ClientSession() as session:
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "\nYou are ChatGPT, a large language model trained by OpenAI. \nKnowledge cutoff: 2023-10\nCurrent model: gpt-4o-mini\nCurrent time: Sun Nov 24 2024 11:49:42 GMT+0300 (Москва, стандартное время)\nLatex inline: \\(x^2\\) \nLatex block: $e=mc^2$\n\n"
                }
            ],
            "stream": True,
            "model": "gpt-4o-mini",
            "temperature": 0.5,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "top_p": 1
        }
        if user_id is not None:
            messages = await get_last_user_messages(user_id=user_id)
            for me in messages:
                x = {"role": me["role"], "content": me["message"]}
                data["messages"].append(x)

        data["messages"].append({"role": "user",
                                 "content": text + "\nОТВЕЧАЙ ТОЛЬКО ЧИСТЫМ ТЕКСТОМ НА РУССКОМ БЕЗ ЛЮБОГО ФОРМАТИРОВАНИЯ ПРЯМ СОВСЕМ"})
        headers = {
            "Accept": "application/json, text/event-stream",
            "Authorization": "Bearer nk-jasper",
            "Content-Type": "application/json",
            "Referer": "https://gpt.jasper.finance/",
            "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A_Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        resp = await session.post("https://gpt.jasper.finance/api/openai/v1/chat/completions", json=data,
                                  headers=headers)
        x = await resp.text()
        x = assemble_text(x)
        return x

async def load_documents():
    documents = {}
    async for doc in collection.find():
        for hash_key, doc_data in doc["documents"].items():
            title = doc_data.get("title", "")
            raw_text = doc_data.get("raw_text", "")
            text = f"{title} {raw_text}"
            documents[hash_key] = text
    return documents

def get_embeddings(texts):
    inputs = tokenizer(texts, return_tensors="tf", padding=True, truncation=True, max_length=128)
    bert_model = TFBertModel.from_pretrained("bert-base-uncased")
    outputs = bert_model(inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()

async def update_document_embeddings():
    global documents, document_embeddings
    documents = await load_documents()
    document_embeddings = get_embeddings(list(documents.values()))

@router.on_event("startup")
async def startup_event():
    await update_document_embeddings()

def find_relevant_documents(query, document_embeddings, documents):
    query_embedding = get_embeddings([query])
    similarities = cosine_similarity(query_embedding, document_embeddings)
    most_relevant_indices = np.argsort(similarities[0])[-4:][::-1]
    return [(list(documents.keys())[i], list(documents.values())[i]) for i in most_relevant_indices]

@router.post("/process_text")
async def process_text(request: TextRequest):
    try:
        business = await get_business_by_id(request.business_id)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")

        business_info = f"Бизнес: {business['name']}, Сфера: {business['sphere']}, Размер: {business['size']}, Тип: {business['type']}, Специализация: {business['specialization']}"

        relevant_documents = find_relevant_documents(request.text, document_embeddings, documents)
        if relevant_documents:
            result = f"Смотри, у меня есть такой вопрос - {request.text} и у меня есть несколько документов (они будут ниже). Сформируй мне ответ на мой вопрос на основе этих документов, и самостоятельно ТОЛЬКО В СЛУЧАЕ ЕСЛИ В ДОКУМЕНТАХ НЕ НАШЛОСЬ ОТВЕТА. Факт о документах в ответе вообще не упоминай. Информация о бизнесе: {business_info}. Сами документы: {' '.join([doc_text for _, doc_text in relevant_documents])}"
            answer = await get_answer_jasper(result, request.user_id)
            await save_user_message(user_id=request.user_id, role="user", message=request.text)
            await save_user_message(user_id=request.user_id, role="system", message=answer)
            return {"result": answer}
        raise HTTPException(status_code=500, detail="Failed to process text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
