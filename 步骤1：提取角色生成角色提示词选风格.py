from 助手 import *
from CommonFunction import *
from SD绘图API import *

文案文件夹 = '拆分文案'
文档集合 = '文档集合'

人物文档 = f'{文档集合}/人物.txt'
角色图片提示词文档 = f'{文档集合}/角色图片提示词.txt'
模型目录 = "F:\AI\sd\models\Stable-diffusion"
角色选型目录 = "图片\角色选型"
段落列表文档 = f'{文档集合}/段落列表.txt'
分镜文档 = f'{文档集合}/分镜.txt'


画角色选型 = False

# 第3步
if not 是否存在(人物文档):
    创建人物(文案文件夹, 人物文档)

# 第4步
if not 是否存在(角色图片提示词文档):
    创建角色图片提示词(人物文档, 角色图片提示词文档)

if 画角色选型:
    wendang = print_key_value_pairs_from_file(角色图片提示词文档)

    #生成角色样板
    for key,value in wendang.items():
        print(f"Key: {key}")
        print(f"Value: {value}")
        print("-" * 40)  # 打印分隔线以区分不同的键值对
        prompt = 写文(f"翻译成英文：{value}")
        print("提示词：",prompt)
        if 画角色选型:
            model_list = filter_files_by_extension(模型目录,".safetensors")
            for model in model_list:
                image_file_name = f"{角色选型目录}\\{key}{model}.png"
                if not 是否存在(image_file_name):
                    print("角色选型路径为：",image_file_name)
                    negative_prompt = "(worst quality,low quality:1.3),logo,watermark,text,(worst quality,low quality:1.3),logo,watermark,text,FastNegativeV2,blurry,low quality,bad anatomy,sketches,lowres,normal quality,monochrome,grayscale,worstquality,signature,cropped,bad proportions,out of focus,username,"
                    try:
                        draw_image_by_prompt_change_model(model,prompt,negative_prompt=negative_prompt,width=512,height=512,output_image_path=image_file_name,sae="DDIM",steps=20)
                    except Exception as e:
                        print("模型：%s有问题，请在sd中检查"%model,e)
                        continue

# 第5步 分镜段落
if not 是否存在(段落列表文档):
    #创建段落列表文档(文案文件夹, 段落列表文档)
    创建段落列表文档自定义(全局配置.原文路径,段落列表文档)

# 第6步 整理分镜格式
if not 是否存在(分镜文档):
    创建分镜文档新版(段落列表文档, 分镜文档, 角色图片提示词文档, 0)