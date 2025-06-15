# Stage 1: Create .env file
FROM python:3 AS builder

# Generate .env with debug-friendly settings
RUN python -c "import secrets; \
    print('SECRET_KEY=' + secrets.token_urlsafe(50)); \
    print('DEBUG=True'); \
    print('ALLOWED_HOSTS=*'); \
    print('DATABASE_URL=sqlite:///db.sqlite3')" > /tmp/.env

FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY core/requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY --from=builder /tmp/.env /app/.env

COPY ./core /app

# Debugging: Show directory structure and environment
RUN echo "===== Debug Information =====" && \
    echo "\nDirectory Structure:" && \
    ls -lR /app && \
    echo "\nEnvironment Variables:" && \
    printenv && \
    echo "\n.env File Content:" && \
    cat /app/.env

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]