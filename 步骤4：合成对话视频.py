from 助手 import *
from CommonFunction import *
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from moviepy.editor import VideoFileClip, concatenate_videoclips

片段列表 = 列表()
对话文案 = '文档集合/对话文案.txt'
# 定义最大线程数
MAX_THREADS = 100
# 创建一个线程列表
threads = []

def save_movie(片段,路径):
    directory = os.path.dirname(路径)

    # 检查目录是否存在，如果不存在则创建目录
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"目录已创建：{directory}")
    else:
        print(f"目录已存在：{directory}")
    片段.保存(路径)


工厂实例 = 视频工厂()
# 等比例缩放的，不要同时设置宽高[1.2]
if 全局配置.视频类型 == '横屏':
    背景尺寸 = 全局配置.竖屏背景尺寸
else:
    背景尺寸 = 全局配置.横屏背景尺寸
视频缩放宽度 = 背景尺寸[0]
# 内容比画幅大1.2倍
输出("视频缩放宽度", 视频缩放宽度)


delete_files_in_directory("临时视频")

所有图片列表 = 遍历文件夹('图片')
conversations = read_json_file(对话文案)

分镜_list = []


for conversation in conversations:
    student_question = conversation.get("学员", "无问题")
    teacher_answer = conversation.get("老师", "无回答")
    分镜_list.append({"学员":student_question})
    分镜_list.append({"老师":teacher_answer})


    # 使用ThreadPoolExecutor来管理线程池

stu_index = 0
tea_index = 0
for scene in 分镜_list:
    # 过滤特殊符号

    if "学员" in scene:
        # 制作学生视频-图文
        标题 = 自动断句(scene["学员"]).连文('')
        纯图片名 = f'{stu_index+1}-学生-{标题}'
        原图片文件 = f'图片/{纯图片名}.png'
        声音文件 = f'声音/{纯图片名}.wav'
        临时视频文件路径 = f'临时视频/{纯图片名}.mp4'
        if not 是否存在(临时视频文件路径):
            音频 = 抓取音频(声音文件)

            视频 = 新建图片视频(原图片文件)
            视频.设置时长(音频.时长)
            视频.缩放(宽度=视频缩放宽度)

            视频.配音(音频)
            背景 = 新建纯色视频((0, 0, 0), 时长=视频.时长, 尺寸=背景尺寸)
            视频.摆放(0, (背景.高 - 视频.高) / 2)

            片段 = 叠加图层(列表(背景, 视频), 背景尺寸=背景尺寸)
            分段添加字幕(scene["学员"], 片段, 音频.时长)
        stu_index += 1
    if "老师" in scene:

        # 制作老师视频-视频
        标题 = 自动断句(scene["老师"]).连文('')
        纯图片名 = f'{tea_index + 1}'
        声音文件 = f'声音/{纯图片名}.wav'
        视频素材文件名 = 纯图片名 + '.mp4'
        视频素材文件路径 = f'视频/{视频素材文件名}'
        临时视频文件路径 = f'临时视频/{纯图片名}.mp4'
        if not 是否存在(临时视频文件路径):
            音频 = 抓取音频(声音文件)
            视频 = 抓取视频(视频素材文件路径)

            视频.缩放(宽度=视频缩放宽度)

            #视频 = 工厂实例.随机转场(视频, 背景尺寸)
            #视频.配音(音频)
            背景 = 新建纯色视频((0, 0, 0), 时长=视频.时长, 尺寸=背景尺寸)
            视频.摆放(0, (背景.高 - 视频.高) / 2)

            片段 = 叠加图层(列表(背景, 视频), 背景尺寸=背景尺寸)
            分段添加字幕(scene["老师"], 片段, 音频.时长)

        tea_index += 1

    if not 是否存在(临时视频文件路径):
        # 如果线程数少于最大值，则创建新线程
        if len(threads) < MAX_THREADS:
            thread = threading.Thread(target=save_movie, args=(片段,临时视频文件路径))
            threads.append(thread)
            thread.start()
        else:
            # 等待任意一个线程完成
            threading.wait(threads)
            # 移除完成的线程
            threads = [t for t in threads if t.is_alive()]
            # 创建新线程
            thread = threading.Thread(target=save_movie, args=(片段,临时视频文件路径))
            threads.append(thread)
            thread.start()


# 等待所有线程完成
for t in threads:
    t.join()

videoclips = []
stu_index = 0
tea_index = 0
for scene in 分镜_list:

    if "学员" in scene:
        标题 = 自动断句(scene["学员"]).连文('')
        纯图片名 = f'{stu_index+1}-学生-{标题}.mp4'
        #视频 = 抓取视频(f'临时视频/{纯图片名}')
        videoclips.append(VideoFileClip(f'临时视频/{纯图片名}'))
        stu_index += 1

    if "老师" in scene:
        纯图片名 = f'{tea_index + 1}'
        视频素材文件名 = 纯图片名 + '.mp4'
        #视频 = 抓取视频(f'临时视频/{视频素材文件名}')
        videoclips.append(VideoFileClip(f'临时视频/{视频素材文件名}'))

        tea_index += 1






final_clip = concatenate_videoclips(videoclips,method="chain")
final_clip.write_videofile('输出视频(静态).mp4',
                                threads=10,
                               logger=None,
                               audio_codec="aac",
                               fps=30)

