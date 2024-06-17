import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()



class RabbitTopicsConfig(Enum):
    NEXT_CLOUD_UPLOAD_FILE: str = os.getenv(
        "NEXT_CLOUD_UPLOAD_FILE", "next_cloud_upload_file")
    NEXT_CLOUD_RESPONSE: str = os.getenv(
        "NEXT_CLOUD_RESPONSE", "next_cloud_response")

class NextCloudConfig(Enum):
    NEXT_CLOUD_HOST: str = os.getenv("NEXT_CLOUD_HOST")
    NEXT_CLOUD_USERNAME: str = os.getenv("NEXTCLOUD_ADMIN_USER")
    NEXT_CLOUD_PASSWORD: str = os.getenv("NEXTCLOUD_ADMIN_PASSWORD")
    NEXT_CLOUD_PREFIX: str = os.getenv("NEXT_CLOUD_PREFIX")
    NEXT_CLOUD_URL = f"{NEXT_CLOUD_HOST}/{NEXT_CLOUD_PREFIX}"
    
class RabbitConfig(Enum):
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT: int = int(os.getenv("RABBITMQ_PORT", 15672))
    RABBITMQ_URL: str = (
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@"
        f"{RABBITMQ_HOST}:{RABBITMQ_PORT}"
    )


class ErrorMessage(Enum):
    SERVICE_UNAVAILABLE_ERROR: str = "Сервис Nextcloud недоступен: {}"

