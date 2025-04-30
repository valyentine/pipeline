import os
import subprocess
import re
import shutil
import time
from glob import glob

# 配置路径映射（根据实际情况修改）
PATH_TO_GLB = {
    "/media/yuliu/新加卷/pipeline/UNDONE/6imZUJGRUq4": "/media/yuliu/新加卷/pipeline/scene/6imZUJGRUq4.basis.glb",
    "/media/yuliu/新加卷/pipeline/UNDONE/gmuS7Wgsbrx": "/media/yuliu/新加卷/pipeline/scene/gmuS7Wgsbrx.basis.glb",
    "/media/yuliu/新加卷/pipeline/UNDONE/jTTGECZYKRA": "/media/yuliu/新加卷/pipeline/scene/jTTGECZYKRA.basis.glb",
    "/media/yuliu/新加卷/pipeline/UNDONE/XNoaAZwsWKk": "/media/yuliu/新加卷/pipeline/scene/XNoaAZwsWKk.basis.glb",
    "/media/yuliu/新加卷/pipeline/UNDONE/yQESfVcg18k": "/media/yuliu/新加卷/pipeline/scene/yQESfVcg18k.basis.glb",
    # 添加更多路径映射...
}

# 自定义休眠时间（单位：秒）
SLEEPTIME = {
    "/media/yuliu/新加卷/pipeline/UNDONE/6imZUJGRUq4": 2.1,
    "/media/yuliu/新加卷/pipeline/UNDONE/gmuS7Wgsbrx": 2.6,
    "/media/yuliu/新加卷/pipeline/UNDONE/jTTGECZYKRA": 1.7,
    "/media/yuliu/新加卷/pipeline/UNDONE/XNoaAZwsWKk": 1.7,
    "/media/yuliu/新加卷/pipeline/UNDONE/yQESfVcg18k": 1.9,
    # 添加更多路径的休眠时间...
}

def process_transformations(traj_dir, glb_path, sleep_time):
    saved_trans = os.path.join(traj_dir, "saved_transformations")
    screenshots = os.path.join(traj_dir, "screenshots")
    if os.path.exists(screenshots):
        print(f"跳过 {traj_dir}（已存在screenshots）")
        return
    
    if not os.path.exists(saved_trans):
        print(f"跳过 {traj_dir}（缺少saved_transformations）")
        return

    txt_files = sorted(glob(os.path.join(saved_trans, "[0-9]*.txt")),
                      key=lambda x: int(os.path.basename(x).split(".")[0]))
    if not txt_files:
        print(f"跳过 {traj_dir}（没有找到txt文件）")
        return

    screenshots_dir = "screenshots"
    if os.path.exists(screenshots_dir):
        shutil.rmtree(screenshots_dir)
    os.makedirs(screenshots_dir, exist_ok=True)

    for idx, txt_file in enumerate(txt_files, 1):
        print(f"正在处理 {os.path.basename(txt_file)} ({idx}/{len(txt_files)})")
        
        cmd = [
            "habitat-viewer",
            glb_path,
            "--agent-transform-filepath",
            txt_file
        ]
        proc = subprocess.Popen(cmd)
        
        time.sleep(sleep_time)  # 使用自定义休眠时间
        
        # 获取窗口ID
        try:
            window_id = subprocess.check_output(
                ["xdotool", "search", "--name", "Viewer"],
                text=True
            ).strip().split()[-1]
        except subprocess.CalledProcessError:
            print("找不到Viewer窗口")
            proc.kill()
            continue

        # 窗口操作
        subprocess.run(["xdotool", "windowsize", window_id, "1280", "720"])
        subprocess.run(["xdotool", "windowfocus", window_id])
        subprocess.run(["xdotool", "key", "--window", window_id, "--delay", "50", "c", "bracketright", "i"])
        time.sleep(0.2)
        subprocess.run(["xdotool", "key", "--window", window_id, "Escape"])
        time.sleep(0.2)
        
        proc.kill()
        proc.wait()

    process_screenshots(screenshots_dir, traj_dir)

def process_screenshots(screenshots_dir, target_dir):
    os.chdir(screenshots_dir)
    
    # 收集并排序目录
    dirs = []
    for d in os.listdir("."):
        if os.path.isdir(d) and re.match(r"\d{4}_\d{1,2}_\d{1,2}_\d{1,2}-\d{1,2}-\d{1,2}", d):
            parts = re.split(r"[-_]", d)
            timestamp = "".join(f"{int(x):02d}" for x in parts)
            dirs.append((timestamp, d))
    
    sorted_dirs = sorted(dirs, key=lambda x: x[0])
    
    # 移动并重命名文件
    count = 1
    for _, d in sorted_dirs:
        src = os.path.join(d, "0.png")
        if os.path.exists(src):
            dest = os.path.join("..", f"{count}.png")
            shutil.move(src, dest)
            count += 1
        shutil.rmtree(d)
    
    os.chdir("..")
    shutil.rmtree(screenshots_dir)
    
    # 移动截图到目标目录
    final_dir = os.path.join(target_dir, "screenshots")
    os.makedirs(final_dir, exist_ok=True)
    for f in glob("*.png"):
        shutil.move(f, os.path.join(final_dir, f))
    
    print(f"已处理 {len(sorted_dirs)} 张截图到 {final_dir}")

def main():
    for base_dir, glb_path in PATH_TO_GLB.items():
        if not os.path.exists(glb_path):
            print(f"跳过 {base_dir}（GLB文件不存在）")
            continue
        
        # 获取自定义休眠时间（默认3秒）
        sleep_time = SLEEPTIME.get(base_dir, 3.0)
        
        # 查找所有traj_*目录（排除traj_0）
        traj_dirs = []
        for d in os.listdir(base_dir):
            if re.match(r"traj_[-+]?\d+$", d) and d != "traj_0":
                traj_dirs.append(os.path.join(base_dir, d))
        
        if not traj_dirs:
            print(f"跳过 {base_dir}（没有找到traj目录）")
            continue
        
        for traj_dir in traj_dirs:
            print(f"\n处理目录: {traj_dir}")
            original_dir = os.getcwd()
            try:
                os.chdir(traj_dir)
                process_transformations(traj_dir, glb_path, sleep_time)
            finally:
                os.chdir(original_dir)

if __name__ == "__main__":
    main()
    print("所有操作已完成！")
