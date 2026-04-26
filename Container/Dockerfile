# ==============================================================================
# Script Name:  Dockerfile
# Description:  Docker file to create a continer helps windows Users 
#               to run on Linux Environment with minmal solution
# Author:       MohammedDiaa (mohammeddiaato@gmail.com)
# Company:      Gestell - Professional Embedded Solutions
# ==============================================================================

FROM ubuntu:latest
#I installed what I found necessity for me
RUN apt-get update && apt-get install -y nginx build-essential python3 python3-pip python3-venv 

WORKDIR /app
#giving all the permissions to the containers to Access everything on this directory

RUN mkdir /workspace && chmod 777 /workspace


#making a virtual envrionment for the flask app that recieves the Files and routes them to work on python because of errors 
RUN python3 -m venv venv

# installing the Flask for the Virtual environment

RUN ./venv/bin/pip install flask

COPY app.py .

COPY nginx.conf /etc/nginx/nginx.conf



EXPOSE 80

CMD nginx && ./venv/bin/python app.py