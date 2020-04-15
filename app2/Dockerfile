FROM quoinedev/python3.7-pandas-alpine 

RUN apt update
RUN apt install -y python3-pip
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "mysite.wsgi:application"]
# ENTRYPOINT ["/usr/local/bin/python", "app.py"]