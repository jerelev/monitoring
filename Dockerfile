from ubuntu:20.04

WORKDIR /app

LABEL com.jfrog.artifactory.retention.maxCount="100"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=/app

RUN apt update && \
    apt install -y python3 python3-pip mount nfs-common --no-install-suggests --no-install-recommends

COPY ./requirements.txt /app/requirements.txt

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade -r requirements.txt

RUN apt-get -y --purge autoremove && rm -rf /var/lib/apt/lists/*

COPY ./ ./

CMD ["python3", "main.py"]