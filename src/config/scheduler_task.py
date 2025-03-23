import logging
from src.drive.backup.backup_db import drive_backup_db
from src.drive.backup.backup_images import drive_backup_images

async def backup_database():
    try:
        logging.info(f"Realizando backup de la base de datos")

        await drive_backup_db()

        await drive_backup_images()
    except Exception as e:
        logging.error(f"Error al hacer la copia de seguridad: {e}")