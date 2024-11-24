import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import docx
import PyPDF2
from striprtf.striprtf import rtf_to_text
import re
import hashlib
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from yarl import URL

async def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Ошибка при обработке DOCX: {e}")
        return ""

async def extract_text_from_rtf(file_path):
    try:
        with open(file_path, 'rb') as f:
            rtf_content = f.read()
        return rtf_to_text(rtf_content.decode('latin1'))
    except Exception as e:
        print(f"Ошибка при обработке RTF: {e}")
        return ""

async def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Ошибка при обработке PDF: {e}")
        return ""

def sanitize_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|\r\n]+', "", filename)
    return filename[:150]

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def is_valid_text(text):
    try:
        text.encode('utf-8').decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

def generate_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

async def fetch(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            print(f"Ошибка при загрузке страницы {url}: {response.status}")
            return None
        return await response.text()

async def download_file(session, url, file_path):
    async with session.get(url) as response:
        if response.status != 200:
            print(f"Ошибка при загрузке файла {url}: {response.status}")
            return None
        with open(file_path, 'wb') as f:
            f.write(await response.read())
        return file_path

async def extract_text_func(file_path, file_extension):
    if file_extension == '.docx':
        return await extract_text_from_docx(file_path)
    elif file_extension == '.rtf':
        return await extract_text_from_rtf(file_path)
    elif file_extension == '.pdf':
        return await extract_text_from_pdf(file_path)
    else:
        print(f'Неизвестный формат файла: {file_extension}')
        return ""

async def process_document(item, category, base_url, session):
    title_element = item.find('h2')
    title = title_element.get_text(strip=True) if title_element else "Без названия"

    description_element = item.find('div', class_='page-section__content')
    description = description_element.get_text(strip=True) if description_element else ""

    document_name = f"{title} {description}".strip()
    document_name = sanitize_filename(document_name)

    download_section = item.find('div', class_='page-simple__download')
    if download_section:
        links = download_section.find_all('a', href=True)
        for link in links:
            if "скачать" in link.get_text().strip().lower():
                file_url = link['href']
                file_extension = os.path.splitext(file_url)[1]
                full_url = URL(base_url).join(URL(file_url))

                file_path = document_name + file_extension
                await download_file(session, full_url, file_path)

                if os.path.exists(file_path):
                    try:
                        text = await extract_text_func(file_path, file_extension)
                        text = clean_text(text)

                        if not is_valid_text(text):
                            print(f"Некорректный текст в файле {file_path}, пропуск...")
                            continue
                    except Exception as e:
                        print(f"Ошибка обработки файла {file_path}: {e}")
                        continue

                    try:
                        os.remove(file_path)
                        print(f"Файл {file_path} успешно удален.")
                    except PermissionError as e:
                        print(f"Ошибка удаления файла {file_path}: {e}")
                    except Exception as e:
                        print(f"Неожиданная ошибка при удалении файла {file_path}: {e}")

                    print(f'Обработан документ: {title}')

                    return {
                        "hash": generate_hash(text),
                        "data": {
                            "date_published": datetime.now(),
                            "title": title,
                            "raw_text": text,
                            "short_text": None,
                            "tags": []
                        }
                    }
                else:
                    print(f"Ошибка: файл {file_path} не был сохранен.")
    return None

async def main():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client.HelpBusiness
    collection = db.Websites

    kuban_links = {
        "Законодательство и официальные документы": "https://mbkuban.ru/documents/zakonodatelstvo-i-ofitsialnye-dokumenty/",
        "Реализация программ государственной поддержки": "https://mbkuban.ru/documents/realizatsiya-programm-gosudarstvennoy-podderzhki/",
        "Единый реестр инвестиционных проектов Краснодарского края": "https://mbkuban.ru/documents/edinyy-reestr-investitsionnykh-proektov-krasnodarskogo-kraya/",
        "Совет по развитию предпринимательства в Краснодарском крае": "https://mbkuban.ru/documents/sovet-po-predprinimatelstvu-pri-glave-administratsii-gubernatore-krasnodarskogo-kraya/",
        "Государственная программа": "https://mbkuban.ru/documents/gosudarstvennaya-programma/"
    }

    async with aiohttp.ClientSession() as session:
        for category, url in kuban_links.items():
            page_content = await fetch(session, url)
            if not page_content:
                continue

            soup = BeautifulSoup(page_content, 'html.parser')
            items = soup.find_all('div', class_='legislation-tabs__item')

            tasks = [process_document(item, category, url, session) for item in items]
            documents_data = await asyncio.gather(*tasks)

            documents = {doc['hash']: doc['data'] for doc in documents_data if doc}

            await collection.update_one(
                {"_id": url},
                {"$set": {"documents": documents}},
                upsert=True
            )
