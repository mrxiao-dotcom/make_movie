import re
from 格式化分镜文档 import *

def count_chinese_characters(text):
    # 使用正则表达式匹配汉字
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    # 返回汉字的数量
    return len(chinese_chars)


def extract_chinese_characters(text):
    # 使用正则表达式匹配中文字符，并保持出现顺序
    return [char for char in re.findall(r'[\u4e00-\u9fff]', text)]

def find_chinese_chars_with_line_numbers(text):
    # 使用正则表达式找到所有中文字符及其在原文中的行数
    chinese_chars_with_line_numbers = []
    lines = text.splitlines()
    for line_number, line in enumerate(lines, start=1):
        for match in re.finditer(r'[\u4e00-\u9fff]', line):
            char = match.group()
            chinese_chars_with_line_numbers.append((char, line_number))
    return chinese_chars_with_line_numbers


def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return ""


def compare_chinese_characters_with_line_numbers(file1, file2):
    content1 = read_file(file1)
    content2 = read_file(file2)

    if not content1 or not content2:
        print("一个或两个文件可能是空的，或者读取文件时出错。")
        return [], []

    chinese_line_numbers1 = find_chinese_chars_with_line_numbers(content1)
    chinese_line_numbers2 = find_chinese_chars_with_line_numbers(content2)
    print("file1 和 file2字数分别是:",len(chinese_line_numbers1),len(chinese_line_numbers2))

    diff = {
        'file1': [],
        'file2': []
    }

    # 对比两个列表中的中文字符及其行数
    for char_line1, char_line2 in zip(chinese_line_numbers1, chinese_line_numbers2):
        if char_line1[0] != char_line2[0]:
            diff['file1'].append((char_line1[0], char_line1[1]))
            diff['file2'].append((char_line2[0], char_line2[1]))
            break  # 只对比到第一个不同之处

    # 如果一个文件中的中文字符比另一个多
    if len(chinese_line_numbers1) > len(chinese_line_numbers2):
        diff['file1'].extend(chinese_line_numbers1[len(chinese_line_numbers2):])
    elif len(chinese_line_numbers2) > len(chinese_line_numbers1):
        diff['file2'].extend(chinese_line_numbers2[len(chinese_line_numbers1):])

    return diff

def compare_chinese_characters_with_line_numbers_file_to_txt(file1, content2):
    content1 = read_file(file1)


    if not content1 or not content2:
        print("一个或两个文件可能是空的，或者读取文件时出错。")
        return [], []

    chinese_line_numbers1 = find_chinese_chars_with_line_numbers(content1)
    chinese_line_numbers2 = find_chinese_chars_with_line_numbers(content2)

    diff = {
        'file1': [],
        'file2': []
    }

    # 对比两个列表中的中文字符及其行数
    for char_line1, char_line2 in zip(chinese_line_numbers1, chinese_line_numbers2):
        if char_line1[0] != char_line2[0]:
            diff['file1'].append((char_line1[0], char_line1[1]))
            diff['file2'].append((char_line2[0], char_line2[1]))
            break  # 只对比到第一个不同之处

    # 如果一个文件中的中文字符比另一个多
    if len(chinese_line_numbers1) > len(chinese_line_numbers2):
        diff['file1'].extend(chinese_line_numbers1[len(chinese_line_numbers2):])
    elif len(chinese_line_numbers2) > len(chinese_line_numbers1):
        diff['file2'].extend(chinese_line_numbers2[len(chinese_line_numbers1):])

    return diff


def check_json_format(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件内容
            data = json.load(file)  # 假设文件是JSON格式

            # 定义期望的格式
            expected_keys = {"角色", "画面", "文案", "特效"}

            # 检查每个元素是否符合格式
            for idx, item in enumerate(data, start=1):
                current_keys = set(item.keys())
                if current_keys != expected_keys:
                    print(f"第{idx}行：缺少或多余的键。期望的键为{expected_keys}，当前的键为{current_keys}")
                else:
                    print(f"第{idx}行：格式正确")

    except json.JSONDecodeError as e:
        print(f"文件内容不是有效的JSON格式: {e}")
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

if __name__ == '__main__':
    print("hi 我是文案校对.py")
    #上传('高阶推文_竖屏短视频尺寸.mp4')

    yuanwen = False
    fenjing = True
    fenjinggao = False

    文档集合 = '文档集合'
    file_path1 = f'{文档集合}/段落列表.txt'
    file_path2 = f'原文.txt'
    input_file_path = '文档集合/分镜.txt'
    ################## 校对原文与分段 ############
    if yuanwen:

        file_path1 = f'{文档集合}/段落列表.txt'
        file_path2 = f'原文.txt'
        diff = compare_chinese_characters_with_line_numbers(file_path1, file_path2)

        print(f"文件1中的差异（字符，位置）: {diff['file1']}",file_path1)
        print(f"文件2中的差异（字符，位置）: {diff['file2']}",file_path2)

    ############### 校对分镜与分段 ###############
    if fenjing:
        json_data = load_json(input_file_path)
        fenjing = ""
        for itor in json_data:
            fenjing += itor['文案']+'\n'
        diff = compare_chinese_characters_with_line_numbers_file_to_txt(file_path1,fenjing)
        print(diff)

    if fenjinggao:

        check_json_format(input_file_path)
        json_data = load_json(input_file_path)