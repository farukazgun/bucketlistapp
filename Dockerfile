FROM python:alpine3.6
COPY . /app
WORKDIR /app
RUN apk --no-cache add  gcc libc-dev libffi-dev mariadb-dev && pip3 install -r requirements.txt
EXPOSE 5000 
ENTRYPOINT [ "python3" ] 
CMD [ "app.py" ]
