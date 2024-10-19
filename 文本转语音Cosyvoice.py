import requests
import json
import os
from pydub import AudioSegment
from CommonFunction import *


AudioSegment.converter = r"D:\ffmpeg\bin\ffmpeg.exe"

def convert_wav_to_mp3(wav_file_path, mp3_file_path):
	# 加载WAV文件
	try:
		audio = AudioSegment.from_wav(wav_file_path)

		# 导出为MP3文件
		audio.export(mp3_file_path, format="mp3")
	except Exception as e:
		print(e)

def convert_txt_to_mp3(text,mp3_file_path,seeds="金牌讲师",speed=1):
    try:
        headers = {'Content-Type': 'application/json'}
        gpt = {"text": text, "speaker": seeds, "streaming": 0,"speed":speed }
        response = requests.post("http://localhost:9880/", data=json.dumps(gpt), headers=headers)
        audio_data = response.content

        path = extract_path_parts(mp3_file_path)
        path_dir = path["directory"]
        if path_dir and not os.path.exists(path_dir):
            os.makedirs(path_dir, exist_ok=True)

        with open(mp3_file_path, "wb") as f:
            f.write(audio_data)

        #convert_wav_to_mp3(wav_file_path, mp3_file_path)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    convert_txt_to_mp3("混帐东西，不会抽，那发面里的烟末是谁撒的？都不会抽吗？好，咱们这就来看看！把口袋翻过来，快点！听见了没有？快翻过来！","test.mp3","万象先生")


