# Use official Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files from your project into the image
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
