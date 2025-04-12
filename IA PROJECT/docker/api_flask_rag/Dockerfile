
FROM python:3.10-slim


RUN pip install --upgrade pip
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY rag_app.py /app/
COPY app.html /app/templates/


EXPOSE 5000

CMD ["python", "rag_app.py"]
