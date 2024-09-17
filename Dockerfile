FROM python:3.11.3

# Maintainer info
LABEL maintainer="your_email@example.com"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Make working directories
WORKDIR /app

# Upgrade pip with no cache
RUN pip install --no-cache-dir -U pip

# Copy application requirements file to the created working directory
COPY requirements.txt .

# Install application dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy every file in the source folder to the created working directory
COPY . .

# Expose the port (optional for Cloud Run)
EXPOSE 8080

# Run the python application using uvicorn directly
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
