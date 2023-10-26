FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json
CMD [ "python", "fetch_secret_and_create_k8s_secret.py" ]
