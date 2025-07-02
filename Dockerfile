# Usa imagem oficial Python 3.11 slim
FROM python:3.11-slim

# Instala ffmpeg e outras dependências necessárias
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Define o diretório da aplicação dentro do container
WORKDIR /app

# Copia requirements.txt e instala dependências Python
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia todo o código para dentro do container
COPY . .

# Comando para rodar seu script principal
CMD ["python", "run.py"]
