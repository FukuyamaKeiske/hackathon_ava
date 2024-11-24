import asyncio
from fastapi import FastAPI
from auth import router as auth_router
from text_processing import router as text_router
from database import init_db
import uvicorn
from logging_config import logger
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import shutil
import os

app = FastAPI()

app.include_router(auth_router, tags=["auth"])
app.include_router(text_router, tags=["text"])

# Функция для бэкапа и очистки логов
def backup_logs():
    date_str = datetime.now().strftime("%Y-%m-%d")
    backup_filename = f'logs/{date_str}_logs.txt.bak'
    shutil.copy('logs/logs.txt', backup_filename)

    # Удаление файлов старше 7 дней
    cutoff_date = datetime.now() - timedelta(days=7)
    for filename in os.listdir('logs'):
        if filename.endswith('.bak'):
            file_date_str = filename.split('_')[0]
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
            if file_date < cutoff_date:
                os.remove(os.path.join('logs', filename))

# Запуск планировщика
scheduler = BackgroundScheduler()
scheduler.add_job(backup_logs, 'cron', hour=0, minute=0, timezone='Europe/Moscow')
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
