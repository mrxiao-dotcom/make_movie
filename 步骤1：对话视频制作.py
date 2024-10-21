import 文本转语音Cosyvoice
from 助手 import *
from CommonFunction import *
import subprocess

#基础文件路径

file_dir = f"文档集合"
audio_dir = f"声音"
pic_dir = f"图片"
movie_dir = f"视频"
dst_dir = f'F:\AI\PicToMovie\in'

auto_init = True #如果需要自动初始化，那么只需要修改这个标志即可
if auto_init:
    delete_files_in_directory(file_dir)
    delete_files_in_directory(audio_dir)
    delete_files_in_directory(pic_dir,"src1.png")
    delete_files_in_directory(movie_dir)
    delete_files_in_directory(dst_dir)
    print("删除工作目录成功")
#说明,步骤1：对话视频制作，负责生成所有的视频，前提是删除所有图片、声音、临时视频、视频的内容
#在图片文件夹中，把要做视频的原图：src1.png放进去，脸部一定要清晰可见

output_file_path = f"{file_dir}/对话文案.txt"
if not 是否存在(output_file_path):
    read_and_convert_to_json(f"原文.txt",output_file_path)

#分别给学员和老师配音
conversations = read_json_file(output_file_path)
student_ask_list = []
teacher_answer_list = []
for index, conversation in enumerate(conversations):
    student_question = conversation.get("学员", "无问题")
    teacher_answer = conversation.get("老师", "无回答")

    标题 = 自动断句(student_question).连文('')
    student_file_path = f"声音/{index+1}-学生-{标题}.wav"
    teacher_file_patn = f"声音/{index+1}.wav"
    if not 是否存在(student_file_path):
        print(f"对话 {index + 1}:")
        print(f"学员：{student_question}")

        文本转语音Cosyvoice.convert_txt_to_mp3(student_question, student_file_path, "温迪迪", 1.1)
    if not 是否存在(teacher_file_patn):
        文本转语音Cosyvoice.convert_txt_to_mp3(teacher_answer, teacher_file_patn, "万象先生中等", 1.1)
        print(f"对话 {index + 1}:")
        print(f"老师：{teacher_answer}\n")

    student_ask_list.append(f"{index+1}-学生-{标题}")

#对口型基材文件夹


student_pic_path = f"图片/src1.png"

#1 把学员的图片，按话术复制
copy_images(student_pic_path,student_ask_list)

#2 把原图，复制到对口型文件夹，按照老师文件夹名
copy_and_rename_image(student_pic_path,dst_dir)

#把文件复制到口型生成目录
src_mp3_dir = f'声音'
copy_numeric_filename_files(src_mp3_dir,dst_dir,False)

#执行对口型批处理
batch_file_path = f'F:\AI\PicToMovie\start_batch.bat'
working_directory = f'F:\AI\PicToMovie'
result = subprocess.run(['cmd.exe', '/c', batch_file_path],   cwd=working_directory)

#再把目标文件夹中的mp4：1-out.mp4,只剩下数字.mp4复制到临时视频文件夹
temp_video_folder = f"视频"
copy_outmp4_and_rename_files(dst_dir,temp_video_folder)

