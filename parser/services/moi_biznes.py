import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import hashlib
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def generate_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

async def fetch(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            print(f"Ошибка при загрузке страницы {url}: {response.status}")
            return None
        return await response.text()

async def save_to_database(link, title, content, collection):
    if not content:
        return

    content_hash = generate_hash(content)
    document = {
        content_hash: {
            "date_published": datetime.now(),
            "title": title,
            "raw_text": content,
            "short_text": None,
            "tags": []
        }
    }

    await collection.update_one(
        {"_id": link},
        {"$set": {"documents": document}},
        upsert=True
    )

async def process_article(session, article, article_base_url, collection):
    title = article.find('div', class_='grid-title').text.strip()
    link = article_base_url + article['href']

    article_content = await fetch(session, link)
    if not article_content:
        return

    article_soup = BeautifulSoup(article_content, 'html.parser')
    container = article_soup.find('div', class_='container-xl')
    if container:
        # Извлекаем текст из всех тегов внутри контейнера
        content = ' '.join(container.stripped_strings)
        content = clean_text(content)
        await save_to_database(link, title, content, collection)
        print(f"Сохранена статья: {title}")

async def main():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client.HelpBusiness
    collection = db.Websites

    base_url = "https://xn--90aifddrld7a.xn--p1ai/knowledge/?PAGEN_1={page_num}"
    article_base_url = "https://xn--90aifddrld7a.xn--p1ai"

    async with aiohttp.ClientSession() as session:
        tasks = []
        for page_num in range(1, 23):
            page_content = await fetch(session, base_url.format(page_num=page_num))
            if not page_content:
                continue

            soup = BeautifulSoup(page_content, 'html.parser')
            articles = soup.find_all('a', class_='grid-card-item')

            for article in articles:
                tasks.append(process_article(session, article, article_base_url, collection))

        await asyncio.gather(*tasks)

    print("Парсинг завершен.")
