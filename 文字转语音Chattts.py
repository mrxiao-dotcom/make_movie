from gradio_client import Client, file
from pydub import AudioSegment

AudioSegment.converter = r"D:\ffmpeg\bin\ffmpeg.exe"


def convert_txt_to_mp3(text,mp3_file_path,speed=1,seeds=1):

	try:
		name = "四川美食确实以辣闻名，但也有不辣的选择。比如甜水面、赖汤圆、蛋烘糕、叶儿粑等，这些小吃口味温和，甜而不腻，也很受欢迎。"
		if text == "":
			text = name

		client = Client("http://127.0.0.1:7860/")
		result = client.predict(
			text_file=text,
			num_seeds=1,
			seed=seeds,  	#声音种子
			speed=speed,	#语速
			oral=0,
			laugh=0,
			bk=2,
			min_length=80,
			batch_size=3,
			temperature=0.1,
			top_P=0.7,
			top_K=20,
			roleid="1",
			refine_text=True,
			api_name="/generate_tts_audio"
		)

		wav_file_path = result
		mp3_file_path = mp3_file_path
		convert_wav_to_mp3(wav_file_path, mp3_file_path)
	except Exception as e:
		print(e)

def convert_wav_to_mp3(wav_file_path, mp3_file_path):
	# 加载WAV文件
	try:
		audio = AudioSegment.from_wav(wav_file_path)

		# 导出为MP3文件
		audio.export(mp3_file_path, format="mp3")
	except Exception as e:
		print(e)

if __name__ == '__main__':
    convert_txt_to_mp3("你好，我叫钢铁侠","test.mp3",7,697)

