FROM python:3.9-slim

WORKDIR /app

# Install dependencies from requirements.txt
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Define the working directory for the container (optional)
ENV PORT=8080
EXPOSE 8080

# Run the Flask app in debug mode
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers=2", "--threads=4", "wsgi:app"]