# Usa uma imagem oficial do Python, otimizada e segura
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos e os instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte do projeto para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação Flask usa
EXPOSE 5000

# Comando para rodar a aplicação quando o container iniciar
CMD ["python", "main.py"]