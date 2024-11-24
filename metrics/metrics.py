import psutil
import time
import os
from shutil import copy2
from datetime import datetime, timedelta

LOG_FILE = "logs.txt"
BACKUP_DIR = "backups"
CPU_THRESHOLD = 80
RAM_THRESHOLD = 80
NETWORK_THRESHOLD = 600000

def create_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    backup_filename = datetime.now().strftime("%Y%m%d_%H%M%S_logs.txt.bak")
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    copy2(LOG_FILE, backup_path)

    # Удаление старых бэкапов
    for filename in os.listdir(BACKUP_DIR):
        backup_file_path = os.path.join(BACKUP_DIR, filename)
        creation_time = datetime.fromtimestamp(os.path.getctime(backup_file_path))
        if datetime.now() - creation_time > timedelta(days=7):
            os.remove(backup_file_path)

def monitor_system():
    while True:
        # Получаем сетевую активность
        net_io_start = psutil.net_io_counters()
        time.sleep(1)
        net_io_end = psutil.net_io_counters()
        network_usage = (net_io_end.bytes_sent + net_io_end.bytes_recv - net_io_start.bytes_sent - net_io_start.bytes_recv) / (1024 * 1024)

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                with proc.oneshot():
                    pid = proc.info['pid']
                    name = proc.info['name']
                    cpu = proc.cpu_percent(interval=0.1)
                    ram = proc.memory_percent()

                    if cpu > CPU_THRESHOLD or ram > RAM_THRESHOLD or network_usage > NETWORK_THRESHOLD:
                        with open(LOG_FILE, "a") as log_file:
                            log_file.write(f"{datetime.now()}, {name}, {pid}, || CPU - {cpu}%; RAM - {ram}%; Network - {network_usage:.2f}MB ||\n")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if datetime.now().hour == 0 and datetime.now().minute == 0:
            create_backup()

        time.sleep(1)

if __name__ == "__main__":
    monitor_system()
