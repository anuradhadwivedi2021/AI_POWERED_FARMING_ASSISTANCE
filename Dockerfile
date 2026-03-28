FROM python:3.10.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 7860

ENV FLASK_APP=app.py

CMD ["python", "app.py"]