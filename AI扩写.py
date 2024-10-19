from 助手 import *
from 本地大语言模型 import *


yuanwen = 抓取TXT('文档集合/洗稿原文.txt')
yy = yuanwen.读()
prompt = f'原文是：{yy},保持原文主要意思不变，对内容进行改写，要求尽量不用专业术语，用通俗易懂的语言'
ret = get_message_from_ai(prompt,"你是一个文案改写大师")
print(ret)