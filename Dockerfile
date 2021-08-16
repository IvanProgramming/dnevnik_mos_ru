FROM python:3.9-alpine
RUN pip install -r requirements
EXPOSE 80
COPY . /app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "80"]
