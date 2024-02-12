import requests
import json
import io
import wave
import pyaudio
import time

class VoicevoxEngine:
    def __init__(self, host="voicevox_network", port=50021):
        self.host = host
        self.port = port

    # 音声再生処理
    def speaker(self, request_data):
        # メモリ展開
        audio = io.BytesIO(request_data.content)

        with wave.open(audio,'rb') as f:
            p = pyaudio.PyAudio() # 音声再生処理

            def _callback(in_data, frame_count, time_info, status):
                data = f.readframes(frame_count)
                return (data, pyaudio.paContinue)

            stream = p.open(format=p.get_format_from_width(width=f.getsampwidth()),
                            channels=f.getnchannels(),
                            rate=f.getframerate(),
                            output=True,
                            stream_callback=_callback)

            # 音声再生
            stream.start_stream()
            while stream.is_active():
                time.sleep(0.1)

            stream.stop_stream()
            stream.close()
            p.terminate()

    # voicevox
    def http_request(self,text=None,speaker=54):
        params = (
            ("text", text),
            ("speaker", speaker)
        )

        # http request
        try:
            request_data = requests.post(
                f"http://{self.host}:{self.port}/audio_query",
                params=params
            )

            request_data = requests.post(
                f"http://{self.host}:{self.port}/synthesis",
                headers={"Content-Type": "application/json"},
                params=params,
                data=json.dumps(request_data.json())
            )

            self.speaker(request_data=request_data)

        # http request error
        except requests.exceptions.RequestException as e:
            print(e)
            return False
