FROM python:3-alpine
RUN apk add --update --no-cache
#RUN apk add python-pip python-dev build-essential
COPY ./v001 /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]