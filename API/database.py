from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from utils import hash_password, verify_password
from datetime import datetime

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.HelpBusiness

async def register_user(email, password):
    if await db.Users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(password)
    user_id = await db.Users.insert_one({
        "email": email,
        "password": hashed_password,
        "businesses": []  # Инициализируем пустой список бизнесов
    })
    return str(user_id.inserted_id)

async def authenticate_user(email, password):
    db_user = await db.Users.find_one({"email": email})
    if not db_user or not verify_password(password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return str(db_user["_id"])

async def add_business(user_id, name, sphere, size, type_, specialization):
    business = {
        "name": name,
        "sphere": sphere,
        "size": size,
        "type": type_,
        "specialization": specialization,
        "messages": []
    }
    result = await db.Users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"businesses": business}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")



async def init_db():
    """
    Инициализирует базу данных, добавляя ссылки из файла links.txt в коллекцию ChatGPTLinks,
    если они еще не существуют.
    """
    with open("links.txt", "r") as file:
        # Читаем все строки из файла и удаляем пробелы в начале и конце каждой строки
        links = [line.strip() for line in file]

    for link in links:
        # Проверяем, существует ли ссылка в коллекции ChatGPTLinks
        existing_link = await db.ChatGPTLinks.find_one({"_id": link})
        if not existing_link:
            # Если ссылка не найдена, вставляем новую запись
            await db.ChatGPTLinks.insert_one({
                "_id": link,  # Устанавливаем _id как саму ссылку
                "requests_made": 0,  # Инициализируем количество запросов
                "last_request_successful": False,  # Флаг успешности последнего запроса
                "total_symbols_generated": 0,  # Общее количество сгенерированных символов
                "total_time_spent": 0  # Общее время, затраченное на генерацию
            })


async def get_chatgpt_links():
    """
    Возвращает все ссылки из коллекции ChatGPTLinks.
    """
    # Используем find() для получения всех документов и преобразуем их в список
    return await db.ChatGPTLinks.find().to_list(None)


async def update_chatgpt_link(link_id, update_data):
    """
    Обновляет данные ссылки в коллекции ChatGPTLinks.

    :param link_id: Идентификатор ссылки
    :param update_data: Данные для обновления (например, количество запросов)
    """
    # Обновляем документ с заданным _id, устанавливая новые данные
    await db.ChatGPTLinks.update_one({"_id": link_id}, {"$set": update_data})


async def save_user_message(user_id, role, message):
    """
    Сохраняет сообщение пользователя в коллекции Users.

    :param user_id: Идентификатор пользователя
    :param role: Роль пользователя (например, 'user' или 'assistant')
    :param message: Текст сообщения
    """
    message_data = {
        "role": role,  # Роль отправителя сообщения
        "datetime": datetime.now(),  # Время отправки сообщения
        "message": message  # Текст сообщения
    }
    # Добавляем новое сообщение в массив messages пользователя
    await db.Users.update_one({"_id": ObjectId(user_id)}, {"$push": {"messages": message_data}})


async def get_last_user_messages(user_id, limit=4):
    """
    Возвращает последние сообщения пользователя.

    :param user_id: Идентификатор пользователя
    :param limit: Количество последних сообщений для возврата
    :return: Список сообщений
    """
    # Находим пользователя по идентификатору
    user = await db.Users.find_one({"_id": ObjectId(user_id)})
    if not user:
        # Если пользователь не найден, выбрасываем исключение
        raise HTTPException(status_code=404, detail="User not found")
    # Возвращаем последние сообщения (по умолчанию 4)
    return user.get("messages", [])[-limit:]


async def get_all_user_messages(user_id):
    """
    Возвращает все сообщения пользователя.

    :param user_id: Идентификатор пользователя
    :return: Список всех сообщений пользователя
    """
    # Находим пользователя по идентификатору
    user = await db.Users.find_one({"_id": ObjectId(user_id)})
    if not user:
        # Если пользователь не найден, выбрасываем исключение
        raise HTTPException(status_code=404, detail="User not found")
    # Возвращаем все сообщения пользователя
    return user.get("messages", [])
