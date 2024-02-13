#!/usr/bin/env python3

from voicevox_client_local import VoicevoxEngineLocal

def main():
    voicevox = VoicevoxEngineLocal()
    voicevox.http_request(text="ういびーむ")

if __name__ == "__main__":
    main()
