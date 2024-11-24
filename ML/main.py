import os
import logging
import tensorflow as tf

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tf.get_logger().setLevel(logging.ERROR)

import numpy as np
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, TFBertForSequenceClassification, TFBertModel

client = MongoClient("mongodb://localhost:27017/")
db = client["HelpBusiness"]
collection = db["Websites"]

documents = {}
for doc in collection.find():
    for hash_key, doc_data in doc["documents"].items():
        title = doc_data.get("title", "")
        raw_text = doc_data.get("raw_text", "")
        text = f"{title} {raw_text}"
        documents[hash_key] = text

print(f"Количество документов: {len(documents)}")

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model_path = "saved_bert_model"

if os.path.exists(model_path):
    use_saved_model = input("Найдена сохранённая модель. Использовать её? (да/нет): ").strip().lower()
    if use_saved_model == "да":
        model = tf.keras.models.load_model(model_path)
        train_model = False
    else:
        model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=6)
        train_model = True
else:
    model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=6)
    train_model = True

if train_model:
    labels = np.random.randint(6, size=(len(documents),))
    texts = list(documents.values())

    train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.1)

    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128, return_tensors="tf")
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128, return_tensors="tf")

    train_dataset = tf.data.Dataset.from_tensor_slices((dict(train_encodings), train_labels)).shuffle(1000).batch(16)
    val_dataset = tf.data.Dataset.from_tensor_slices((dict(val_encodings), val_labels)).batch(16)

    # Добавление дропаута для регуляризации
    model.layers[-1].rate = 0.3

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=5e-5),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=["accuracy"])

    model.fit(train_dataset, validation_data=val_dataset, epochs=20)  # Увеличено количество эпох

    model.save(model_path)

# Получение эмбеддингов для документов
def get_embeddings(texts):
    inputs = tokenizer(texts, return_tensors="tf", padding=True, truncation=True, max_length=128)
    bert_model = TFBertModel.from_pretrained("bert-base-uncased")
    outputs = bert_model(inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()

document_embeddings = get_embeddings(list(documents.values()))

def find_relevant_documents(query, document_embeddings, documents):
    query_embedding = get_embeddings([query])
    similarities = cosine_similarity(query_embedding, document_embeddings)
    most_relevant_indices = np.argsort(similarities[0])[-4:][::-1]
    return [(list(documents.keys())[i], list(documents.values())[i]) for i in most_relevant_indices]

query = input("Вопрос >>> ")
relevant_documents = find_relevant_documents(query, document_embeddings, documents)
print("Наиболее релевантные документы:")
for hash_key, doc_text in relevant_documents:
    print(f"{hash_key}: {doc_text}")
