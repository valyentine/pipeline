import argparse
import subprocess
import time
import sys

def check_xdotool_installed():
    try:
        subprocess.run(['xdotool', '--version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: xdotool is required but not installed. Please install xdotool first.")
        sys.exit(1)

def main():
    # 检查xdotool是否安装
    check_xdotool_installed()

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Habitat Viewer窗口分辨率设置工具')
    parser.add_argument('-S', '--scene', required=True, help='场景文件路径（如：file/das.glb）')
    args = parser.parse_args()

    # 启动habitat-viewer
    try:
        viewer_process = subprocess.Popen(['habitat-viewer', args.scene])
    except FileNotFoundError:
        print(f"错误：未找到habitat-viewer可执行文件")
        sys.exit(1)

    # 等待并查找Viewer窗口
    window_id = None
    max_attempts = 30  # 最多尝试30次（约15秒）
    for _ in range(max_attempts):
        try:
            # 查找包含"Viewer"名称的窗口
            result = subprocess.run(
                ['xdotool', 'search', '--name', 'Viewer'],
                capture_output=True,
                text=True,
                check=True
            )
            window_ids = result.stdout.strip().split()
            
            if window_ids:
                window_id = window_ids[0]  # 取第一个匹配的窗口
                print(f"找到Viewer窗口，ID：{window_id}")
                break
        except subprocess.CalledProcessError:
            pass
        
        time.sleep(0.5)
    else:
        print("错误：未能在指定时间内找到Viewer窗口")
        viewer_process.terminate()
        sys.exit(1)

    # 设置窗口分辨率
    try:
        subprocess.run(
            ['xdotool', 'windowsize', window_id, '2560', '1440'],
            check=True
        )
        print("成功设置窗口分辨率为2560x1440")
    except subprocess.CalledProcessError as e:
        print(f"设置分辨率时出错：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
