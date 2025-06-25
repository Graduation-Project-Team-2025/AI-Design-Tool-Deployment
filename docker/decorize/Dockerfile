FROM ghcr.io/astral-sh/uv:0.7.15-python3.12-bookworm-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libavif-dev pkg-config \
    libjpeg-dev \
    libgl1 \
    gcc unzip zip \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt .

ARG HUGGINGFACE_TOKEN
ENV HUGGINGFACE_TOKEN=${HUGGINGFACE_TOKEN}

RUN uv pip install --system --no-cache-dir huggingface_hub transformers

RUN python -c "from huggingface_hub import login; import os; login(token=os.environ['HUGGINGFACE_TOKEN'])"
RUN python -c "from huggingface_hub import snapshot_download; \
snapshot_download(repo_id='BertChristiaens/controlnet-seg-room', use_auth_token=True, local_dir='./assets/models-weights/controlnet')" 

RUN python -c "from huggingface_hub import snapshot_download(repo_id='runwayml/stable-diffusion-v1-5', use_auth_token=True, local_dir='./assets/models-weights/base-model')"

RUN python -c "from huggingface_hub import snapshot_download(repo_id='Helsinki-NLP/opus-mt-ar-en', use_auth_token=True, local_dir='./assets/models-weights/translator')"


RUN uv pip install -r requirements.txt --system

COPY src/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
