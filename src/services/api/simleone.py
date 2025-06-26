import aiohttp
import asyncio
import logging
from src.core.config import Config
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

class SimpleOneAPI:
    # инициализация по настройкам из конфига
    def __init__(self):
        self.base_url = Config.SIMPLEONE_URL
        self.api_key = Config.SIMPLEONE_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    # создание нового тикета
    async def create_ticket(self, email: str, category: str, subcategory: str,
                          description: str, attachments: List[str] = None) -> Optional[Dict]:
        ticket_data = {
            "type": Config.DEFAULT_TICKET_TYPE,
            "priority": Config.DEFAULT_PRIORITY,
            "title": f"{category} - {subcategory}",
            "description": description,
            "custom_fields": {
                "category": category,
                "subcategory": subcategory,
                "user_email": email
            }
        }

        if attachments:
            ticket_data["attachments"] = attachments

        url = f"{self.base_url}/api/v1/tickets"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, json=ticket_data) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            print(f"Ошибка при создании тикета: {e}")
            return None

    # получение списка тикетов пользователя
    async def get_user_tickets(self, email: str) -> Optional[List[Dict]]:
        query = {
            "query": {
                "type": Config.DEFAULT_TICKET_TYPE,
                "custom_fields.user_email": email
            },
            "fields": ["id", "title", "status", "created_at"],
            "sort": [{"field": "created_at", "order": "desc"}]
        }

        url = f"{self.base_url}/api/v1/tickets/search"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, json=query) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data.get("data", [])
        except asyncio.CancelledError:
            logger.info("Запрос отменён")
            raise
        except Exception as e:
            logger.error(f"Ошибка при получении тикетов: {str(e)}")
            return None

    # обновление тикета (добавление вложений/текста)
    async def add_comment_to_ticket(self, ticket_id: str, comment: str,
                                  attachments: List[str] = None) -> bool:
        comment_data = {
            "text": comment
        }
        if attachments:
            comment_data["attachments"] = attachments

        url = f"{self.base_url}/api/v1/tickets/{ticket_id}/comments"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, json=comment_data) as response:
                    response.raise_for_status()
                    return True
        except Exception as e:
            print(f"Ошибка при добавлении комментария: {e}")
            return False