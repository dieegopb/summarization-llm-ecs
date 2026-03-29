# Use imagem oficial Python leve
FROM python:3.13-slim

# Evita geração de arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Força logs aparecerem direto no terminal
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia requirements primeiro (melhor cache de build)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Comando padrão
ENTRYPOINT ["python", "-m", "app.main"]
# CMD ["python", "app/main.py"]