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
WORKDIR /TicketService_FastAPI_Streamlit/

COPY . /TicketService_FastAPI_Streamlit/

RUN ls -al /TicketService_FastAPI_Streamlit/


# Install package from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

