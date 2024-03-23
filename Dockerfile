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

# Mount the local code directory as a volume
VOLUME ["app"]

# Run the Flask app in debug mode
CMD ["python", "./app.py"]