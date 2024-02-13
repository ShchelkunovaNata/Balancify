FROM python:3.11-slim
RUN apt-get update && apt-get install make
WORKDIR /apps/WalletWise
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "manage.py", "runserver"]