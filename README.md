# pipeline
使用habitat模拟器进行无人机室内飞行轨迹收集pipeline
# 1. 环境准备

## 1.1 Conda 环境配置

```bash
conda create -n habitat python=3.8 cmake
conda activate habitat
```
## 1.2 Habitat-sim 安装

```bash
conda install habitat-sim=0.2.0 -c aihabitat -c conda-forge
```
安装 2.0 版本即可，如需安装其他版本，请根据对应版本调整 Python 版本。

# 2. 测试使用
## 2.1 场景文件下载
**HM3D** 可通过网盘下载;
**Gibson** 可通过[此处](https://dl.fbaipublicfiles.com/habitat/data/scene_datasets/gibson_habitat.zip)下载;
**MP3D** 可通过以下命令下载：

  ```bash
  python download_mp.py --task habitat -o /path/to/your/dataset/  
  ```
## 2.2 打开场景
使用类似下列命令打开场景测试：
```
habitat-viewer path/to/your/scene/1LXtFkjw3qL.glb
```
可以使用wasd控制水平移动，zx控制垂直移动，↑↓←→控制相机视角转动，更多详细操作可参照[教程](https://github.com/GuoPingPan/Habitat-Sim-Usage-Chinese)

:warning: 在后续采集轨迹时请仅使用w,a,d,z,x以及←→键进行控制

# 3. 轨迹采集
## 3.1 场景文件准备
将需要的场景文件复制到pipeline目录下，并新建对应的轨迹文件夹
```
cp /path/to/1LXtFkjw3qL.glb /path/to/pipeline/
mkdir 1LXtFkjw3qL
