import  文本转语音Cosyvoice
import SD绘图API

from 助手 import *
from 文字转语音Baidu import *


ai_model_voice = "local" #如果服务器种子用完了，采用本地
ai_model_write = "not local"
ai_model_draw = "local"

分镜文档 = '文档集合/分镜与提示词.txt'
序号 = 0
wendang = 阅读分镜文档JSON(分镜文档)

negative_prompt = "(worst quality,low quality:1.3),logo,watermark,text,(worst quality,low quality:1.3),logo,watermark,text,FastNegativeV2,blurry,low quality,bad anatomy,sketches,lowres,normal quality,monochrome,grayscale,worstquality,signature,cropped,bad proportions,out of focus,username,"
for 分镜 in wendang:
    # 实现风格/人物统一：1、一致性；2、种子；
    台词 = 分镜.获取('文案')
    # 过滤特殊符号
    标题 = 自动断句(台词).连文('')
    纯文件名 = f'{序号}-{标题}'
    图片文件 = f'图片/{纯文件名}.png'
    if not 是否存在(图片文件):
        prompt = 分镜.获取('提示词')
        输出(f'图片提示词翻译结果：{prompt}')
        if ai_model_draw == "local":


            SD绘图API.draw_image_by_prompt_change_model(全局配置.模型, prompt,negative_prompt,512,512,图片文件,全局配置.采样器,25)

        else:
            画图(prompt, 场景=全局配置.场景, 保存位置=图片文件, 尺寸=全局配置.尺寸,
                 模型=全局配置.模型, 编码器=全局配置.编码器, 微调=全局配置.微调)

    声音文件 = f'声音/{纯文件名}.mp3'


    if not 是否存在(声音文件):
        if ai_model_voice == "local":
            ## 这是chattts版
            #文字转语音Chattts.convert_txt_to_mp3(台词,声音文件,1,697)  #697 女生 nice  #6531 京味普通话 #1649 不错
            ## 这是百度
            #文字转语音Baidu.convert_txt_to_mp3(台词, 声音文件)
            ## 这是阿里巴巴
            #文字转语音alibaba.convert_txt_to_mp3(台词,声音文件)
            ## 这是阿里巴巴的cosyVoice
            pass
            文本转语音Cosyvoice.convert_txt_to_mp3(台词,声音文件,"台湾女生",1.1)
        else:
            朗读(台词, 保存位置=声音文件, 音色=全局配置.音色, 音量=全局配置.朗读音量, 语速=全局配置.语速, 情感=全局配置.情感)


        """
        解说音频 = 抓取音频(声音文件)
        解说音频.波形图(尺寸=(15, 10), 路径=f'调音/压缩前.png')
        解说音频.压缩(阈值=-50, 比例=6, 启动时间=10, 释放时间=100)
        解说音频.波形图(尺寸=(15, 10), 路径=f'调音/压缩后.png')
        解说音频.信号增强(55)
        解说音频.波形图(尺寸=(15, 10), 路径=f'调音/增强后.png')
        解说音频.保存('调音/增强后.mp3', 码率=None)
        解说音频.限幅(阈值=0, 统计=True)
        解说音频.波形图(尺寸=(15, 10), 路径=f'调音/限幅后.png')
        #解说音频.静音缩短(静音阈值=-30, 最短静音时长=100, 淡入淡出时间=3)
        #解说音频.波形图(尺寸=(15, 10), 路径=f'调音/静音缩短.png')
        解说音频.保存(声音文件)
        """

    序号 += 1
