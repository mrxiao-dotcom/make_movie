import json
import os
import shutil

def print_key_value_pairs_from_file(file_path):
    try:
        # 打开文件并加载JSON数据
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data
    except FileNotFoundError:
        print("The file was not found.")
    except json.JSONDecodeError:
        print("The file is not a valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")


def filter_files_by_extension(directory, extension):
    # 检查扩展名是否以点开头
    if not extension.startswith('.'):
        extension = '.' + extension

    # 存储符合条件的文件
    filtered_files = []

    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名
            if file.endswith(extension):
                # 提取文件名和后缀
                name, ext = os.path.splitext(file)
                filtered_files.append(name)

    return filtered_files

def contains_chinese(s):
    return any('\u4e00' <= char <= '\u9fff' for char in s)

def read_and_convert_to_json(input_file, output_file):
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # 将文本对话转换为列表
    dialogues = text.split("学生：")
    conversation_list = []

    for dialogue in dialogues[1:]:  # 跳过第一个空字符串
        lines = dialogue.split("\n")
        student_question = lines[0].strip()
        teacher_answer = ""
        for line in lines[1:]:
            if line.startswith("老师："):
                teacher_answer = line[len("老师："):].strip()
                break
        if teacher_answer:
            conversation_list.append({
                "学员": student_question,
                "老师": teacher_answer
            })

    # 确保输出文件的目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # 将列表转换为JSON并保存到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(conversation_list, f, ensure_ascii=False, indent=4)

def read_json_file(file_path):
    # 确保文件存在
    if not os.path.exists(file_path):
        print("文件不存在，请检查路径。")
        return []

    # 读取JSON文件并解析数据
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def extract_path_parts(file_path):
    # 提取文件的目录路径
    dir_path = os.path.dirname(file_path)
    # 提取文件名（包括扩展名）
    file_name = os.path.basename(file_path)
    # 提取文件扩展名
    file_extension = os.path.splitext(file_name)[1]
    # 提取不包含扩展名的文件名
    file_name_without_extension = os.path.splitext(file_name)[0]

    return {
        "directory": dir_path,
        "file_name": file_name,
        "file_extension": file_extension,
        "file_name_without_extension": file_name_without_extension
    }


def copy_images(src_file, dest_names):
    # 确保源文件存在
    if not os.path.exists(src_file):
        print(f"源文件 {src_file} 不存在，请检查路径。")
        return

    # 获取源文件的目录和扩展名
    src_dir = os.path.dirname(src_file)
    file_extension = os.path.splitext(src_file)[1]

    # 复制图片
    for name in dest_names:
        # 构建目标文件的完整路径
        dest_file = os.path.join(src_dir, f"{name}{file_extension}")
        if not os.path.exists(dest_file):
            # 复制文件
            shutil.copy(src_file, dest_file)
            print(f"图片已复制为：{name}{file_extension}")


def clear_directory(directory):
    # 检查目录是否存在
    if os.path.exists(directory):
        # 遍历目录中的所有文件和文件夹
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            # 如果是文件，则删除
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # 如果是目录，则递归删除
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        # 如果目录不存在，则创建它
        os.makedirs(directory, exist_ok=True)
        print(f"目标目录 {directory} 已创建。")


def copy_numeric_filename_files(src_dir, dst_dir, clear=True):
    # 清空目标目录
    if clear:
        clear_directory(dst_dir)

    # 检查源目录是否存在
    if not os.path.exists(src_dir):
        print(f"源目录 {src_dir} 不存在。")
        return

    # 遍历源目录下的所有文件
    file_list = os.listdir(src_dir)
    for filename in file_list:
        name, ext = os.path.splitext(filename)
        # 检查文件名是否为纯数字
        if name.isdigit():
            # 构建完整的文件路径
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_dir, filename)
            if not os.path.exists(dst_file):
                # 复制文件
                shutil.copy(src_file, dst_file)
                print(f"文件 {filename} 已复制到 {dst_dir}")


def copy_and_rename_image(src_image_path, dst_directory):
    # 检查源图片是否存在
    if not os.path.exists(src_image_path):
        print("源图片不存在。")
        return

    # 检查目标目录是否存在，如果不存在则创建
    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory, exist_ok=True)

    # 获取源图片的扩展名
    src_extension = os.path.splitext(src_image_path)[1]

    # 构建目标图片的完整路径（文件名改为“1”，扩展名保持不变）
    dst_image_path = os.path.join(dst_directory, f"1{src_extension}")

    # 复制源图片到目标目录，并重命名
    shutil.copy(src_image_path, dst_image_path)
    print(f"图片已复制并重命名为：{dst_image_path}")


def copy_outmp4_and_rename_files(source_dir, target_dir):
    """
    Copy files from source directory to target directory and rename them.

    Args:
    source_dir (str): The path to the source directory.
    target_dir (str): The path to the target directory.

    Returns:
    None
    """
    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)

    # 遍历源目录中的所有文件
    for filename in os.listdir(source_dir):
        if filename.endswith('-out.mp4'):
            # 构造完整的文件路径
            source_file = os.path.join(source_dir, filename)
            # 构造目标文件名（去掉'-out'并改为大写扩展名）
            target_file = os.path.join(target_dir, filename[:-8] + '.MP4')
            # 复制文件

            if not os.path.exists(target_file):
                shutil.copy(source_file, target_file)
                print(f'Copied and renamed {filename} to {target_file}')


def delete_files_in_directory(directory, exclude_files=None):
    # 如果没有提供排除文件列表，则创建一个空列表
    if exclude_files is None:
        exclude_files = []

    # 检查目录是否存在
    if not os.path.exists(directory):
        print("目录不存在。")
        return

    # 遍历目录中的所有文件和子目录
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # 判断文件是否需要被排除
        if filename in exclude_files:
            print(f"文件 {filename} 被排除，跳过删除。")
            continue

        # 判断是文件还是目录
        if os.path.isfile(file_path) or os.path.islink(file_path):
            # 删除文件或链接
            os.remove(file_path)
            print(f"已删除文件：{file_path}")
        elif os.path.isdir(file_path):
            # 如果是目录，则递归删除
            shutil.rmtree(file_path)
            print(f"已删除目录：{file_path}")