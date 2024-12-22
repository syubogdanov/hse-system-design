FROM python:3.9

RUN pip install prometheus_client
RUN pip install environs
RUN pip install requests

WORKDIR .
COPY . .
CMD ["python" , "prober.py"]