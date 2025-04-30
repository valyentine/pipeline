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
**HM3D 场景** 可通过网盘下载。
**Gibson 数据集** 可通过此链接下载：[Gibson 数据集](https://dl.fbaipublicfiles.com/habitat/data/scene_datasets/gibson_habitat.zip)
**MP3D 数据集** 可通过以下命令下载：

  ```bash
  python download_mp.py --task habitat -o path/to/your/dataset/  
  ```
