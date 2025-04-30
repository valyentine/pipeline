import argparse
import os
import re
import time

def get_sorted_txt_files(directory):
    """获取目录下按数字排序的txt文件列表"""
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    files.sort(key=lambda x: int(x.split('.')[0]))
    return [os.path.join(directory, f) for f in files]

def are_files_equal(file1, file2):
    """比较两个文件内容是否完全相同"""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        return f1.read().strip() == f2.read().strip()

def process_removal(directory):
    """删除冗余文件"""
    files = get_sorted_txt_files(directory)
    if not files:
        return

    retained = []
    for i in range(len(files) - 1):
        if not are_files_equal(files[i], files[i+1]):
            retained.append(files[i])
    retained.append(files[-1])

    redundant = set(files) - set(retained)
    for file in redundant:
        os.remove(file)

def extract_number(filename):
    """从文件名中提取数字（若文件名为纯数字+.txt格式）"""
    match = re.fullmatch(r'(\d+)\.txt', filename)
    return int(match.group(1)) if match else None

def process_rename(directory):
    """重命名文件为连续序号"""
    # 收集所有符合条件的文件并提取数字
    files = []
    for fname in os.listdir(directory):
        num = extract_number(fname)
        if num is not None:
            files.append((num, fname))
    
    if not files:
        return

    # 按数字升序排序
    files.sort(key=lambda x: x[0])

    # 生成唯一临时前缀
    temp_prefix = f"temp_{int(time.time())}_"

    # 阶段1：重命名为临时文件
    temp_files = []
    for num, fname in files:
        temp_name = temp_prefix + fname
        src = os.path.join(directory, fname)
        dest = os.path.join(directory, temp_name)
        os.rename(src, dest)
        temp_files.append((num, temp_name))

    # 阶段2：按序重命名
    for idx, (_, temp_name) in enumerate(temp_files, start=1):
        new_name = f"{idx}.txt"
        src = os.path.join(directory, temp_name)
        dest = os.path.join(directory, new_name)
        os.rename(src, dest)

def main():
    parser = argparse.ArgumentParser(description='删除冗余帧并重命名文件')
    parser.add_argument('-P', '--path', required=True, help='目录路径（多个用逗号分隔）')
    args = parser.parse_args()
    
    for dir_path in args.path.split(','):
        dir_path = dir_path.strip()
        if not os.path.isdir(dir_path):
            print(f"警告：目录不存在 '{dir_path}'")
            continue
        
        # 先删除冗余文件
        process_removal(dir_path)
        # 再重命名剩余文件
        process_rename(dir_path)

if __name__ == "__main__":
    main()
