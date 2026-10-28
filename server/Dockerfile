FROM python:3.11-slim

WORKDIR /app

# Create non-root system user with dedicated home directory
RUN useradd -u 10001 -m -d /home/appuser -s /bin/bash appuser && \
    mkdir -p /home/appuser/.cache && chown -R appuser:appuser /home/appuser

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/content-agent/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]