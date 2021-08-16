FROM python:3.9-alpine
COPY . /app
RUN pip install -r /app/requirements.txt
EXPOSE 80
WORKDIR /app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port",  "80"]
