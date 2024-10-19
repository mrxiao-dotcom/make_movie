from 助手 import *
from 本地大语言模型 import *
from CommonFunction import *


local_write = "not local"



def make_fenjing_to_prompt():


    fenjing_path = '文档集合/分镜.txt'
    output_path = '文档集合/分镜与提示词.txt'
    文档集合 = '文档集合'
    角色图片提示词文档 = f'{文档集合}/角色图片提示词.txt'
    角色图片提示词 = 抓取TXT(角色图片提示词文档).读()

    new_fenjing_list = 列表()
    for 分镜 in 阅读分镜文档(fenjing_path):

        data  = dict()

        台词 = 分镜.获取('文案')
        角色 = 分镜.获取('角色')
        画面 = 分镜.获取('画面')
        print(台词,角色,画面) ##


        prompt = f'找到{角色}在{角色图片提示词}的键值，加上{画面}的内容,翻译成英文关键词，关键词之间用逗号隔开，不要增加任何其他标点符号，不要写关键词之外的内容'
        if local_write == "local":
            ret = get_message_from_ai(prompt,"你是一个Stable Diffusion 提示词 设计大师,擅长理解文义，设计匹配的图片提示词")
        else:
            ret = 写文(prompt)
        print(ret)
        if contains_chinese(ret):
            prompt = f'把{ret}中的内容，翻译成英文'
            if local_write == "local":
                ret = get_message_from_ai(prompt,"你是一个Stable Diffusion 提示词 设计大师,擅长理解文义，设计匹配的图片提示词")
            else:
                ret = 写文(prompt)

        data.update({"文案":台词})
        data.update({"提示词":ret})


        new_fenjing_list.添加(data)

    新文档 = TXT(output_path, 格式='文本')
    新文档.写(new_fenjing_list)
    新文档.保存()

def repair_prompt_to_english():
    output_path = '文档集合/分镜与提示词.txt'
    new_fenjing_list = 列表()
    wendang = 阅读分镜文档JSON(output_path)
    for 分镜 in wendang:
        data = dict()

        wenan =  分镜.获取('文案')
        prompt = 分镜.获取('提示词')
        if contains_chinese(prompt):
            print("发现不正确的提示词:",prompt)
            prompt = f'把{prompt}中的内容，翻译成英文'
            if local_write == "local":
                ret = get_message_from_ai(prompt,"你是一个Stable Diffusion 提示词 设计大师,擅长理解文义，设计匹配的图片提示词")
            else:
                ret = 写文(prompt)
            prompt = ret
            print("已经修正：",ret)

        data.update({"文案": wenan})
        data.update({"提示词": prompt})

        new_fenjing_list.添加(data)

    新文档 = TXT(output_path, 格式='文本')
    新文档.写(new_fenjing_list)
    新文档.保存()

if __name__ == '__main__':
    make_fenjing_to_prompt()
    repair_prompt_to_english()