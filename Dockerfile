
# O Dockerfile é um arquivo de texto que contém instruções para construir uma imagem Docker. Ele define o ambiente necessário para executar uma aplicação, incluindo o sistema operacional, dependências e configurações específicas.

# Construindo a base da Imagem
# Usa uma versão oficial do Python 
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala apenas o essencial, mas com um timeout maior e sem as dependências de compilação
# Caso não precise do git dentro do container, ele foi removido para evitar erro
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia o código para dentro da imagem
# Copia o arquivo de dependências e instala as bibliotecas
COPY requirements.txt .

# Instalação de Dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Copiar a pasta .streamlit com o secrets.toml
COPY .streamlit/ .streamlit/

# Comando de Iniciaçização (Portas Abertas)
# Comando para rodar o Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]




