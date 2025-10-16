FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose FastAPI port
EXPOSE $API_PORT

# Start FastAPI server
CMD uvicorn main:app --host $API_HOST --port $API_PORT