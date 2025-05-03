FROM python:3.12.9-slim

WORKDIR /root

COPY requirements.txt .
RUN apt-get update && apt-get install -y git  # Needed to install git packages from requirements.txt
RUN pip install -r requirements.txt

COPY app.py .

ENTRYPOINT ["python"]
CMD ["app.py"]
