FROM python:3-slim-buster
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY main.py main.py
CMD ["python","main.py"]


#FROM scratch
#COPY requirements.txt /requirements.txt
#RUN pip install -r /requirements.txt
#COPY main.py main.py
#CMD ["python","main.py"]