FROM python:3.9-slim

# Update and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    vim \
    ssh \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*


# set working directory /
WORKDIR /

# Copy from github repository by corngang
ADD https://github.com/corngang/TicketService_FastAPI_Streamlit/archive/refs/heads/main.tar.gz main.tar.gz
RUN tar -xvf main.tar.gz
RUN rm -rf main.tar.gz

# Set working directory
WORKDIR /TicketService_FastAPI_Streamlit/

# Install package from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set env
#ENV PORT=8000

# Open port
#EXPOSE 8000

# Run command in container
#CMD ["python3", "login_api/login.py"]
