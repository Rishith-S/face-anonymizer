FROM python:3.11-slim

# Install system packages for OpenCV + MediaPipe
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

# Set up app directory
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set Streamlit config
ENV STREAMLIT_PORT=7860
ENV STREAMLIT_HEADLESS=true

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
