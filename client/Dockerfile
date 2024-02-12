FROM python:3.7
# アプリケーションディレクトリを作成する

WORKDIR /usr/src/python 
COPY . .

# pipのアップデート
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y portaudio19-dev
RUN pip install -r requirements.txt
# アプリケーションコードをコンテナにコピー

CMD [ "python", "main.py" ]
