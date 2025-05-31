# Utilizando uma imagem Python como base
FROM python:3.12-slim-bookworm

# Define o diretório de trabalho
WORKDIR /projeto

# Copia os requisitos e instala as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Copia o restante do projeto
COPY . .

# Define variáveis de ambiente para o Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_PORT=5003
ENV FLASK_RUN_HOST=0.0.0.0

# Expõe a porta da aplicação
EXPOSE 5003

# Comando para rodar a aplicação
CMD ["flask", "run"]
