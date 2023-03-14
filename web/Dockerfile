FROM python:3.11-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80
COPY .. .
CMD ["python", "-m", "app"]
