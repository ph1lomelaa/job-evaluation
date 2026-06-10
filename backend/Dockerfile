FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY jeval ./jeval

EXPOSE 8000

CMD ["uvicorn", "jeval.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
