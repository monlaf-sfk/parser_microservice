
import asyncio
import httpx
from bs4 import BeautifulSoup
from broker import broker_obj


@broker_obj.task
async def parse_website_task(url: str) -> dict:
    print(f"Начинаю парсинг: {url}")

    await asyncio.sleep(3)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "No title"
    print(f"Парсинг завершен: {title}")
    return {"url": url, "title": title, "status": "done"}