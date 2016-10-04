FROM python:3.5

WORKDIR /usr/src/app

RUN pip install --upgrade pip

RUN pip install git+https://github.com/bigchaindb/bigchaindb.git
RUN bigchaindb -y configure
