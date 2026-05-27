FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY requirements-extras.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-extras.txt

COPY . .

# Add entrypoint script and make executable
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PATH="/root/.local/bin:$PATH"

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
