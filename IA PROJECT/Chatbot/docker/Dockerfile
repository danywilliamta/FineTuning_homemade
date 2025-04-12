
FROM python:3.10-slim


RUN pip install --upgrade pip
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY model_llm.py /app/
COPY chatbot_app.py /app/


EXPOSE 5000

CMD ["python", "chatbot_app.py"]
