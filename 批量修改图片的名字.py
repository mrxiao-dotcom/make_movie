from 助手 import *
import os
import re


# 示例用法
folder_path = '图片'  # 替换为你的文件夹路径

files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
original_files = {}

# 构建原始文件名到新文件名的映射
for file in files:
    # 使用正则表达式匹配"序号-名字"格式的文件名
    match = re.match(r'(\d+)-(.+)', file)
    if match:
        original_files[int(match.group(1))] = file
分镜文档 = '文档集合/分镜.txt'
index = 0
for 分镜 in 阅读分镜文档(分镜文档):
    # 实现风格/人物统一：1、一致性；2、种子；
    台词 = 分镜.获取('文案')
    # 过滤特殊符号
    标题 = 自动断句(台词).连文('')
    纯文件名 = f'{index}-{标题}'
    图片文件 = f'图片/{纯文件名}.png'
    if index in original_files:
        # 构建完整的旧文件路径和新文件路径
        old_file = os.path.join(folder_path, original_files[index])

        # 重命名文件
        os.rename(old_file, 图片文件)
        print(f"重命名 '{original_files[index]}' 为 '{图片文件}'")
    else:
        print(f"警告: 序号 {index} 在文件夹中没有找到对应的文件")



    index += 1