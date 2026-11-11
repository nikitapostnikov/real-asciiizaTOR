FROM python:3.14.7-slim

WORKDIR /ascii-script

COPY requierments.txt .

RUN pip install --no-cache-dir -r requierments.txt

COPY ./scriptiq/ /ascii-script/scriptiq/

CMD ["python","scriptiq/ascii-script/__main__.py"]