import requests
import json
import io
import wave
import pyaudio
import time
from requests.exceptions import Timeout

def main():
    requests_info = {
        "host": "localhost",
        "port": 50021
    }
    text = "中村さんそは眠らない"
    
    sample_file = "sanso.wav"
    sounds = Sounds(sample_file)
    # sounds.playwavfile()

    voicevox = Voicevox(requests_info["host"], requests_info["port"])
    voicevox.speak(text=text)

class Voicevox:
    def __init__(self,host="127.0.0.1",port=50021):
        self.host = host
        self.port = port

    def speak(self,text=None,speaker=54): # spaker_id = ななひら
        params = (
            ("text", text),
            ("speaker", speaker)
        )

        try:
            init_q = requests.post(
                f"http://{self.host}:{self.port}/audio_query",
                params=params
            )

            res = requests.post(
                f"http://{self.host}:{self.port}/synthesis",
                headers={"Content-Type": "application/json"},
                params=params,
                data=json.dumps(init_q.json())
            )
        # http request error
        except requests.exceptions.RequestException as e:
            print(e)
            return False

        # メモリ展開
        audio = io.BytesIO(res.content)

        with wave.open(audio,'rb') as f:
            # 音声再生処理
            p = pyaudio.PyAudio()

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


class Sounds:
    def __init__(self, filename):
        self.filename = filename

    def playwavfile(self):
        try:
            wf = wave.open(self.filename, "r")
        except Exception as e:
            print(e)
            return False
            
        # ストリームを開く
        try:
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            # 音声再生
            chunk = 1024
            data = wf.readframes(chunk)
            while data != '':
                stream.write(data)
                data = wf.readframes(chunk)
            stream.close()
            p.terminate()

            # プロンプトが帰ってきてない(error)
            return 0

        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
