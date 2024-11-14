FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-django pytest-asyncio aiohttp websockets

COPY . .

EXPOSE 8000

CMD ["pytest", "test_app.py", "--disable-warnings"]