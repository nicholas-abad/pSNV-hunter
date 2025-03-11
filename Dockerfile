# Use an official lightweight Python image
FROM python:3.11-slim

# Install system dependencies required for building packages
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Clone the GitHub repository
RUN git clone https://github.com/nicholas-abad/pSNV-hunter.git /app/pSNV-hunter

# Change working directory to the cloned repo
WORKDIR /app/pSNV-hunter

# Set up an entrypoint script to pull updates before running the app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Install dependencies (Fix: Ensure GCC and other build tools are installed first)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by the app
EXPOSE 8050

# Run the entrypoint script, which pulls the latest code and starts the app
ENTRYPOINT ["/entrypoint.sh"]