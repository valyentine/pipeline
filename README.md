# pipeline
使用habitat模拟器进行无人机室内飞行轨迹收集pipeline
# 1. 环境准备

## 1.1 Conda 环境配置

```bash
conda create -n habitat python=3.8 cmake
conda activate habitat

## 1.2 Habitat-sim 安装

```bash
conda install habitat-sim=0.2.0 -c aihabitat -c conda-forge

安装 2.0 版本即可，如需安装其他版本，请根据对应版本调整 Python 版本。
