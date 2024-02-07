FROM python:3.7
# アプリケーションディレクトリを作成する
WORKDIR /usr/src/python 
# pipのアップデート
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y portaudio19-dev
COPY requirements.txt ./
RUN pip install -r requirements.txt
# アプリケーションコードをコンテナにコピー
COPY . .
EXPOSE 8080
CMD [ "python", "main.py" ]
