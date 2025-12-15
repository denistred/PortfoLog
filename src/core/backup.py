import os
import subprocess
from pathlib import Path
from datetime import datetime
import aiohttp

from src.core.config import YANDEX_DISK_TOKEN, POSTGRES_HOST, POSTGRES_USER, POSTGRES_DB, POSTGRES_PORT, \
    POSTGRES_PASSWORD

YANDEX_API = "https://cloud-api.yandex.net/v1/disk/resources/upload"


class DatabaseBackupService:
    @staticmethod
    def create_postgres_backup() -> Path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = Path(f"/tmp/backup_{timestamp}.sql")

        env = os.environ.copy()
        env["PGPASSWORD"] = POSTGRES_PASSWORD

        subprocess.run(
            [
                "pg_dump",
                "-h", POSTGRES_HOST,
                "-p", POSTGRES_PORT,
                "-U", POSTGRES_USER,
                "-d", POSTGRES_DB,
                "-f", str(backup_path),
            ],
            check=True,
            env=env,
        )

        return backup_path

    @staticmethod
    async def upload_to_yandex_disk(file_path: Path, token: str, remote_dir: str):
        headers = {"Authorization": f"OAuth {token}"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                    YANDEX_API,
                    params={
                        "path": f"{remote_dir}/{file_path.name}",
                        "overwrite": "true",
                    },
            ) as resp:
                data = await resp.json()
                print(data)
                upload_url = data["href"]

            with open(file_path, "rb") as f:
                async with session.put(upload_url, data=f) as upload_resp:
                    upload_resp.raise_for_status()

    @staticmethod
    async def backup_and_upload():
        print("Creating backup")
        backup_file = DatabaseBackupService.create_postgres_backup()

        print("Uploading to Yandex Disk")
        await DatabaseBackupService.upload_to_yandex_disk(
            file_path=backup_file,
            token=YANDEX_DISK_TOKEN,
            remote_dir="/tmp",
        )

        backup_file.unlink(missing_ok=True)
        print("Backup completed")