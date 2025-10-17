FROM python:3.12-slim

WORKDIR /app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ /app/api/

# Expose FastAPI port
EXPOSE $API_PORT

# Start FastAPI server
CMD uvicorn api.main:app --host $API_HOST --port $API_PORT