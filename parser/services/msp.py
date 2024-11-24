import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

def sanitize_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|\r\n]+', "", filename)
    return filename[:150]

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def generate_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

async def fetch(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        return None

async def parse_page(session, url):
    page_content = await fetch(session, url)
    if not page_content:
        return None

    soup = BeautifulSoup(page_content, 'html.parser')

    # Извлечение заголовка
    title_tag = soup.find('h1', class_='title page-intro__title')
    title = title_tag.get_text(strip=True) if title_tag else 'Без названия'
    title = sanitize_filename(title)

    # Извлечение основного текста
    content_div = soup.find('div', class_='news-detail__content')
    if content_div:
        content = content_div.get_text(separator='\n', strip=True)
        content = clean_text(content)
    else:
        content = 'Текст не найден'

    # Подготовка данных для базы данных
    document = {
        "_id": url,
        "hash": generate_hash(content),
        "data": {
            "date_published": datetime.now(),
            "title": title,
            "raw_text": content,
            "short_text": None,
            "tags": []
        }
    }
    
    return document

async def main():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client.HelpBusiness
    collection = db.Websites

    urls = [
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/sravnenie-sistem-nalogooblozheniya/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/elektronnaya-podpis/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-pravilno-sostavit-ustav-yuridicheskogo-litsa-na-primere-ooo/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kakaya-pravovaya-forma-luchshe-podoydet-dlya-vedeniya-predprinimatelskoy-deyatelnosti/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/sots-predprinimatelstvo/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/otkrytie-biznesa-chto-ne-zabyt-sdelat-v-pervye-tri-mesyatsa/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/zachem-nuzhen-raschyetnyy-schyet-i-kak-ego-otkryt/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/formirovanie-ustavnogo-i-dobavochnogo-kapitala/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/registratsiya-biznesa-ne-vykhodya-iz-doma/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/reestr-subektov-msp-kto-i-kak-v-nego-popadaet-i-chto-delat-v-sluchae-isklyucheniya/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-pravilno-uvolit-rabotnika/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/oformlenie-grazhdansko-pravovogo-dogovora/-base/detail/strakhovye-vznosy-za-sotrudnikov-v-nalogovuyu-sluzhbu/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-predprinimatelyu-oformit-doverennost-/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/dokumenty-naym-rabotnikov/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/spetsialnye-normy-trudovogo-zakonodatelstva-dlya-otdelnykh-kategoriy-rabotnikov/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-oformit-dogovor-polnoy-materialnoy-otvetstvennosti/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-oformlyayutsya-otpuska/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/zachem-nuzhno-shtatnoe-raspisanie-i-kak-ego-oformit/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/strakhovye-vznosy-za-sotrudnikov-3/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/oformlenie-grazhdansko-pravovogo-dogovora/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/sposoby-obespecheniya-ispolneniya-obyazatelstv-/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-pravilno-oformit-dogovor/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/zachem-i-kak-oformlyayutsya-dokumenty-po-dogovoram/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/chto-delat-esli-narushaetsya-dogovor/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-proverit-kontragenta-na-blagonadezhnost-do-podpisaniya-dogovora/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/vybor-nalogovogo-rezhima-2/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/osvobozhdenie-ot-naloga-na-imushchestvo/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/strakhovye-vznosy-individualnogo-predprinimatelya-za-sebya/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/strakhovye-vznosy-za-sotrudnikov/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/uproshchennaya-bukhgalterskaya-otchetnost-dlya-msp/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/osobennosti-vedeniya-individualnym-predprinimatelem-knigi-ucheta-dokhodov-i-raskhodov-/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/otchetnost-v-nalogovuyu/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/otchetnost-po-otkhodam-proizvodstva/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kogda-mozhet-priyti-proverka-biznesa/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-podgotovitsya-k-proverke-chto-nuzhno-znat/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-obzhalovat-rezultat-proverki/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/zashchita-prav-potrebiteley-kak-oformit-ugolok-potrebitelya-vozvrashchat-i-obmenivat-tovary/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/sertifikatsiya-i-deklarirovanie-produktsii/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/otchetnost-po-otkhodam-proizvodstva-2/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/obrabotka-personalnykh-dannykh-klientov-i-sotrudnikov/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/trebovaniya-k-reklame/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/sposoby-obespecheniya-ispolneniya-obyazatelstv-2/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-podgotovitsya-k-proverke-chto-nuzhno-znat-2/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-proverit-kontragenta-na-blagonadezhnost-do-podpisaniya-dogovora-2/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/chto-delat-esli-kontragent-narushil-dogovor-2/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-obzhalovat-rezultat-proverki-2/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/osvobozhdenie-ot-naloga-na-imushchestvo-2/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/pomeshchenie-dlya-biznesa-/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/formirovanie-ustavnogo-i-dobavochnogo-kapitalov/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/intellektualnaya-sobstvennost-kak-zaregistrirovat-tovarnyy-znak/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/dogovor-franchayzinga-na-chto-nuzhno-obratit-vnimanie/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/pokupka-ili-prodazha-biznesa-na-primere-ooo/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/ustanovka-nestatsionarnogo-torgovogo-obekta/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-poluchit-zayem-na-razvitie-biznesa-na-lgotnykh-usloviyakh/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/bukhgalterskaya-otchyetnost-uproshchyennye-formy-dlya-subektov-msp/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-ip-vesti-knigu-uchyeta-dokhodov-i-raskhodov/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/raschetnyy-schet/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-formiruetsya-ustavnyy-i-dobavochnyy-kapitaly-2/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/sistema-bystrykh-platezhey-chto-vazhno-znat/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/mekhanizm-finansovoy-podderzhki-promyshlennoy-kooperatsii-v-eaes/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-poluchit-status-rossiyskogo-subekta-msp/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/kak-zaregistrirovat-biznes-v-sootvetstvii-s-zakonodatelstvom-rf/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/osobennosti-vedeniya-predprinimatelskoy-deyatelnosti/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/lgotnoe-strakhovanie-ot-voennykh-riskov/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/programmy-podderzhki-v-sfere-promyshlennosti/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/programmy-podderzhki-v-sfere-apk/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/podderzhka-pri-vykhode-na-vneshnie-rynki/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/preimushchestva-pri-uchastii-v-zakupkakh/",
        "https://xn--l1agf.xn--p1ai/services/knowledge-base/detail/servisy-dlya-markirovki-produktsii-sredstvami-identifikatsii-/"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [parse_page(session, url) for url in urls]
        documents_data = await asyncio.gather(*tasks)
    
    

    # Обновление базы данных
    for doc in documents_data:
        if doc:
            true_data = {doc['hash']: doc['data']}
            await collection.update_one(
                {"_id": doc['_id']},
                {"$set": {"documents": true_data}},
                upsert=True
            )
