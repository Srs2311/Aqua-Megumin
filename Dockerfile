FROM python:3

WORKDIR /usr/src/app

ENV TZ="America/Denver"
RUN date

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir ./image_library/
RUN mkdir ./pictures/
RUN mkdir ./json/

COPY *.py ./
COPY ./run.sh ./
COPY ./pictures/* ./pictures

RUN chmod a+x run.sh

CMD ["./run.sh"]
