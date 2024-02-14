#!/usr/bin/env python3

from voicevox_client_local import VoicevoxEngineLocal

def main():
    voicevox = VoicevoxEngineLocal()
    voicevox.http_request(text="インベタのさらにインは空中に描くラインだ。高低差の大きいいろは坂特有のヘアピンカーブだからこそ実現可能な掟破りの地元走りだ。この勝負勝った")

if __name__ == "__main__":
    main()
