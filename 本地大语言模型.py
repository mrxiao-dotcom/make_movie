from openai import OpenAI

from openai import OpenAI
import os


def get_message_from_qwenmax(content):

    client = OpenAI(
        api_key="sk-3c261ba6ef3247b091ffd75e674234bc", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )
    completion = client.chat.completions.create(
        model="qwen-max-latest",
        messages=[
            {'role': 'system', 'content': '你是一个文案处理专家.'},
            {'role': 'user', 'content': content}]
        )
    return completion.choices[0].message.content



def get_message_from_ai(content,role='你是一个文案处理专家.'):

    client = OpenAI(
        base_url='http://localhost:11434/v1/',
        api_key='ollama',  # required but ignored
    )


    chat_completion = client.chat.completions.create(
        messages=[
            {'role': 'system', 'content': role},
            {'role': 'user', 'content': content}],
        #model='gemma2:9b',
        model='qwen2.5:7b',
        #model='wangshenzhi/gemma2-9b-chinese-chat:latest',
        #model='qwen:7b'
        #model='llama3:latest'
        stream=False
    )

    ret = chat_completion.choices[0].message.content


    return ret

if __name__ == '__main__':
    ret = get_message_from_ai("中国的首都是哪里")
    print(ret)