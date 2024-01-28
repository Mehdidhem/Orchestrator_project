FROM python:3.8

WORKDIR /app

RUN apt-get update && apt-get install -y openssh-client && rm -rf /var/lib/apt/lists/*

COPY key_pubz /home/user/.ssh/pub_key

RUN chmod 600 /home/user/.ssh/pub_key

# 
RUN eval $(ssh-agent -s) && ssh-add /home/user/.ssh/pub_key

COPY requirements.txt requirements.txt

# le script qui est chargé de l'orchestration des logs
COPY app_parallele.py app_parallele.py

RUN pip install -r requirements.txt

CMD [ "python","app_parallele.py" ]
