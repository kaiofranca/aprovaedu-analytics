FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# --- Diretório de trabalho ---
WORKDIR /app

# --- Dependências do sistema ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# --- Instalar dependências Python ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copiar o código do projeto ---
COPY . .

# --- Executar o pipeline (ETL + Modelo) ---
RUN python main.py

# --- Expor a porta do Streamlit ---
EXPOSE 8501

# --- Comando de inicialização ---
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
