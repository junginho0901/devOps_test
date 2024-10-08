# FROM jenkins/jenkins:lts

# USER root

# RUN apt-get update && \
#     apt-get -y install apt-transport-https \
#     ca-certificates \
#     curl \
#     gnupg2 \
#     zip \
#     unzip \
#     software-properties-common && \
#     curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg > /tmp/dkey; apt-key add /tmp/dkey && \
#     add-apt-repository \
#     "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
#     $(lsb_release -cs) \
#     stable" && \
#     apt-get update && \
#     apt-get -y install docker-ce

FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]