import os
def rename_files(directory):
    """
    Rename files in the given directory by replacing '-aibl' with '-out'.

    Args:
    directory (str): The path to the directory containing files to rename.

    Returns:
    None
    """
    # 确保目录存在
    if not os.path.isdir(directory):
        print("The specified directory does not exist.")
        return

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        # 检查文件名是否符合预期的模式
        if filename.endswith('-aibl.mp4'):
            # 构造新的文件名
            new_filename = filename.replace('-aibl', '-out')
            # 构造完整的文件路径
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)

            # 重命名文件
            os.rename(old_file, new_file)
            print(f"Renamed '{filename}' to '{new_filename}'")


# 使用示例
dst_dir = f'F:\AI\PicToMovie\in'
rename_files(dst_dir)