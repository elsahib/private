FROM quoinedev/python3.7-pandas-alpine 

RUN apk update
RUN apk install -y python3
RUN apk install -y python3-pip
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "app:app"]
# ENTRYPOINT ["/usr/local/bin/python", "app.py"]