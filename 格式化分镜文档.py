import json
import os
import random
import re


def extract_sentences(text):
    # 使用正则表达式匹配句子，包括中英文的句号、感叹号、问号和换行符
    # 同时确保这些符号不在引号内
    sentences = re.split(r'(?<![\'"])[。？！；\n]', text)

    # 定义一个空列表来存储清洗后的句子
    cleaned_sentences = []

    for sentence in sentences:
        # 去除句子中的引号
        cleaned_sentence = re.sub(r'["\'“”‘’]+', '', sentence)
        # 去除句子两端的空白字符
        cleaned_sentence = cleaned_sentence.strip()
        # 过滤掉空字符串
        if cleaned_sentence:
            cleaned_sentences.append(cleaned_sentence)

    return cleaned_sentences


def format_and_write_json(input_file_path, output_file_path):
    """
    读取原始的TXT文件内容，并将其格式化为JSON格式后写入新文件。
    """
    try:
        # 读取原始文件内容
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()

        # 将单引号替换为双引号
        content = content.replace("'", '"').replace("\n", '')

        # 将内容解析为JSON
        data = json.loads(content)

        # 标准化键名
        data = [standardize_keys(item) for item in data]

        # 将JSON对象格式化为字符串
        formatted_content = json.dumps(data, indent=4, ensure_ascii=False)

        # 写入格式化后的内容到新文件
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(formatted_content)

        print(f"File has been formatted and written to {output_file_path}")
    except json.JSONDecodeError:
        print(f"Error: The content of {input_file_path} is not valid JSON.")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} does not exist.")

def load_json(file_path):
    """
    从指定路径加载JSON文件。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def save_json(data, file_path):
    """
    将数据保存到指定路径的JSON文件。
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def validate_and_update_effects(json_data, effects_folder, empty=0):
    """
    验证JSON数据中的“特效”字段是否存在于特效文件夹中，如果不存在则替换为空字符串。
    同时标准化键名。
    """
    # 获取特效文件夹中的所有文件名
    effect_files = set(os.listdir(effects_folder))
    effect_list = list(effect_files)
    print("为分镜随机设计特效...")
    for item in json_data:
        # 标准化键名
        item.update(standardize_keys(item))

        effect_file = item.get('特效')

        # 检查特效文件是否存在于文件夹中
        if effect_file not in effect_files:

            texiao = random.choice(effect_list)
            if empty == 0: #这个标识如果等于0，那么不要特效，否则随机指派特效
                item['特效'] = ""
            else:
                item['特效'] = texiao
            print("特效：%s"%texiao)

    return json_data

def standardize_keys(item):
    """
    标准化字典项的键名，确保其符合预期的格式，并按顺序重命名。
    """
    expected_keys = ['画面', '角色', '文案', '特效']
    new_item = {}

    # 映射表，用于将可能的键名映射到标准键名
    key_mapping = {
        'environment': '环境',
        'env': '环境',
        'scene': '环境',
        'character': '角色',
        'role': '角色',
        'char': '角色',
        'dialogue': '文案',
        'line': '文案',
        'effect': '特效',
        'fx': '特效',
        # 可以在此处添加更多映射
    }

    # 处理每个键值对，并重命名键名
    for key, value in item.items():
        new_key = key_mapping.get(key.lower(), key)  # 尝试映射键名
        if new_key in expected_keys:
            new_item[new_key] = value

    # 确保所有预期的键都存在，如果缺少则添加空字符串
    for ek in expected_keys:
        new_item.setdefault(ek, '')

    return new_item

# 如果连续几个分镜，主角相同，则合并到一起
def merge_consecutive_entries(input_file_path, output_file_path):
    # 从文件读取文本内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 初始化合并后的列表
    merged_data = []
    current_entry = None

    for entry in data:
        # 如果当前条目与前一条目的"角色"相同，则合并"文案"
        if current_entry and entry["角色"] == current_entry["角色"]:
            current_entry["文案"] += " " + entry["文案"]
        else:
            # 如果不相同，将前一条目（如果有的话）添加到合并后的列表中
            if current_entry:
                merged_data.append(current_entry)
            # 设置当前条目为新的条目
            current_entry = entry

    # 添加最后一条目到合并后的列表中
    if current_entry:
        merged_data.append(current_entry)

    # 将处理后的数据转换回JSON格式的字符串
    processed_text = json.dumps(merged_data, indent=4, ensure_ascii=False)

    # 保存处理后的文本到文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(processed_text)

    print(f"处理后的文本已保存到: {output_file_path}")

#如果缺失：特效 ，则补特效
def process_file_and_save(input_file_path, output_file_path):
    # 从文件读取文本内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 将文本转换为JSON对象
    data = json.loads(text)

    # 遍历列表中的每个字典对象
    for item in data:
        # 如果"特效"键不存在，则添加它并赋予空字符串作为默认值
        if "特效" not in item:
            item["特效"] = ""

    # 将处理后的数据转换回JSON格式的字符串
    processed_text = json.dumps(data, indent=4, ensure_ascii=False)

    # 保存处理后的文本到文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(processed_text)

    print(f"处理后的文本已保存到: {output_file_path}")



if __name__ == '__main__':
    # 文件夹路径
    effects_folder = r'特效'  # 请替换为实际的特效文件夹路径
    input_file_path = '文档集合/分镜.txt'  # 请替换为实际的原始文件路径
    output_file_path = '文档集合/分镜.txt'  # 请替换为实际的目标文件路径
    json_file_path = '文档集合/分镜.txt'  # 请替换为实际的目标文件路径

    # 格式化并写入JSON文件
    format_and_write_json(input_file_path, output_file_path)

    #补特效模块
    processed_text = process_file_and_save(input_file_path, output_file_path)

    #合并模块
    merge_consecutive_entries(input_file_path, output_file_path)


    # 加载JSON数据
    json_data = load_json(output_file_path)
    print(json_data)

    # 验证并更新特效字段
    updated_json_data = validate_and_update_effects(json_data, effects_folder, 0)

    # 保存更新后的JSON数据
    save_json(updated_json_data, json_file_path)



    print("分镜文件已更新。")