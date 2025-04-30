#!/bin/bash

# 保存目录设置
target_dir="./saved_transformations"
counter=1

# 创建保存目录（如果不存在）
mkdir -p "$target_dir"

# 清理可能存在的旧计数器文件（可选）
# rm -f "$target_dir"/*.txt 2>/dev/null

# 启动文件监控
inotifywait -m -e create --format "%f" "$target_dir" | while read filename
do
    # 只处理符合命名规范的文件
    if [[ "$filename" =~ ^camera\.[0-9]{4}_[0-9]+_[0-9]+_[0-9]+-[0-9]+-[0-9]+\.txt$ ]]; then
        # 构造完整文件路径
        original="$target_dir/$filename"
        new_name="$target_dir/$counter.txt"
        
        # 执行重命名
        mv "$original" "$new_name"
        echo "已重命名：$filename -> $counter.txt"
        
        # 更新计数器
        ((counter++))
    fi
done
