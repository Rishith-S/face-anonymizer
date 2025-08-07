FROM python:3.11-slim

# Install OpenCV / MediaPipe system dependencies
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 10000
CMD streamlit run app.py --server.port=10000 --server.address=0.0.0.0
