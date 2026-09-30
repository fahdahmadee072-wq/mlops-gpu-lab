FROM python:3.12-slim

WORKDIR /app

# 1) PyTorch from the cu126 channel — the last official build that supports your Pascal GPU.
#    Biggest + slowest layer, and rarely changes → put it FIRST so Docker caches it.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cu126

# 2) The other libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Your code LAST — it changes most often, so only this layer rebuilds on code edits
COPY app/ ./app/

# Where Hugging Face saves downloaded models inside the container
ENV HF_HOME=/models

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
