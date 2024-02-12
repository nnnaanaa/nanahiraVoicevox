from voicevox_client import VoicevoxEngine
from voicevox_client_local import VoicevoxEngineLocal

def main():
    print("Starting")
    # voicevox = VoicevoxEngine()
    voicevox = VoicevoxEngine()
    voicevox.http_request(text="こんにちは")

if __name__ == "__main__":
    main()
