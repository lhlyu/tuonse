FROM python

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip install -r requirements.txt

COPY . /

EXPOSE 5000

CMD ["python", "main.py"]