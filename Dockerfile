FROM python:3.11-slim

# Install system packages required for OpenCV + MediaPipe
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ENV STREAMLIT_PORT=8080
ENV STREAMLIT_HEADLESS=true

EXPOSE 8080

CMD streamlit run app.py --server.port=8080 --server.address=0.0.0.0
