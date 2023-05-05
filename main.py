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
    text = "おはよう"

    weather = WeatherForecast()
    weather.get_weather_forecast_area_code()
    # weather.get_weather_forecast()

    # sample_file = "sanso.wav"
    # sounds = Sounds(sample_file)
    # sounds.playwavfile()

    # voicevox = VoicevoxEngine(requests_info["host"], requests_info["port"])
    # voicevox.speak(text=text)

class VoicevoxEngine:
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
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(chunk)
            stream.close()
            p.terminate()
            return 0

        except Exception as e:
            print(e)

class WeatherForecast:
    def __init__(self):
        pass

    def get_weather_forecast_area_code(self):
        try:
            area_code_url = "https://www.jma.go.jp/bosai/common/const/area.json"
            area_code_json = requests.get(area_code_url).json()
            area_code_list = list(area_code_json["offices"].keys())
            area_name_list = [_["name"] for _ in area_code_json["offices"].values()]
            # zip()関数を使用して、keysとvaluesをまとめて1つのイテレータにする
            pairs = zip(area_name_list, area_code_list)

            # dict()関数を使用して、タプルのリストを辞書に変換する
            area_dict = dict(pairs)
            return area_dict
        except Exception as e:
            print(e)
            return False

    def get_weather_forecast(self):

        # 東京地方のエリアコード
        # ![エリアコード](https://www.jma.go.jp/bosai/common/const/area.json)
        area_code = "130000"
        jma_url = F"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"

        # タイムアウト設定
        jma_json = requests.get(jma_url).json()

        with open('./sample.json', 'w') as f:
            json.dump(jma_json, f, sort_keys=True, indent=4, ensure_ascii=False)

        jma_date = jma_json[0]["timeSeries"][0]["timeDefines"][0]
        jma_area = jma_json[0]["timeSeries"][0]["areas"][0]["area"]["name"]
        jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
        jma_wind = jma_json[0]["timeSeries"][0]["areas"][0]["winds"][0]
        
        # 全角スペース削除
        jma_weather = jma_weather.replace('　', '')
        jma_wind = jma_wind.replace('　', '')

        print(jma_date)
        print(jma_area)
        print(jma_weather)
        print(jma_wind)

if __name__ == "__main__":
    main()
