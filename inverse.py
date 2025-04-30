import os
import re
import argparse

def process_trajectories(target_dir):
    # 遍历目标目录下的所有子目录
    for dir_name in os.listdir(target_dir):
        dir_path = os.path.join(target_dir, dir_name)
        if not os.path.isdir(dir_path):
            continue
        
        # 匹配traj_正数格式的目录
        match = re.match(r'^traj_(\d+)$', dir_name)
        if not match:
            continue
        
        traj_num = int(match.group(1))
        saved_dir = os.path.join(dir_path, 'saved_transformations')
        if not os.path.exists(saved_dir):
            print(f"警告：{saved_dir} 不存在，跳过处理")
            continue

        # 收集并排序所有txt文件
        txt_files = []
        for f in os.listdir(saved_dir):
            if f.endswith('.txt') and f[:-4].isdigit():
                txt_files.append((int(f[:-4]), f))
        
        if not txt_files:
            print(f"警告：{saved_dir} 中没有有效文件，跳过处理")
            continue
        
        txt_files.sort()
        
        # 创建输出目录
        output_dir = os.path.join(target_dir, f'traj_{-traj_num}', 'saved_transformations')
        os.makedirs(output_dir, exist_ok=True)

        # 逆序处理文件
        for new_idx, (orig_num, fname) in enumerate(reversed(txt_files), start=1):
            with open(os.path.join(saved_dir, fname), 'r') as f:
                content = f.read().strip()
            
            elements = content.split()
            if len(elements) < 11:
                print(f"警告：{fname} 元素不足11个，跳过处理")
                continue
            
            # 修改指定位置
            for idx in [0, 2, 8, 10]:
                try:
                    elements[idx] = str(-float(elements[idx]))
                except ValueError:
                    pass
            
            # 写入新文件
            output_path = os.path.join(output_dir, f"{new_idx}.txt")
            with open(output_path, 'w') as f:
                f.write(' '.join(elements) + '\n')

        print(f"已处理 {dir_name} -> traj_{-traj_num}")

def main():
    parser = argparse.ArgumentParser(description='处理轨迹转换数据')
    parser.add_argument('-P', '--path', required=True, help='包含traj_*子目录的目标路径')
    args = parser.parse_args()
    process_trajectories(args.path)

if __name__ == "__main__":
    main()
