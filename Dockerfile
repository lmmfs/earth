FROM python:3.12-slim

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ /app/api/

# Set ownership of the application code and the entrypoint script to the non-root user
RUN chown -R appuser:appuser /app

# Expose FastAPI port
EXPOSE $API_PORT

# Start FastAPI server
CMD python -m uvicorn api.main:app --host $API_HOST --port $API_PORT