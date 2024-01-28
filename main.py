from nanahira import VoicevoxEngine

def main():
    voicevox = VoicevoxEngine()
    voicevox.http_request(text="こんにちは")

if __name__ == "__main__":
    main()
