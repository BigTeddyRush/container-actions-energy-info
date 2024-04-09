# app/Dockerfile

ARG PASSWORD_DB

FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PASSWORD=$PASSWORD_DB

# RUN git clone https://github.com/streamlit/streamlit-example.git .
# Kopiere die lokale streamlit_app.py Datei in das Arbeitsverzeichnis im Docker-Image
COPY streamlit_app.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
