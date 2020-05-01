FROM python:3.6

WORKDIR /data/run

COPY ./requirements.txt ./

RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple/

COPY . .

CMD ["./main.py"]
