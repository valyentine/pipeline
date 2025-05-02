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
```

## 3.2 采集轨迹
使用start.py打开场景，该脚本可调整模拟器分辨率，可以根据具体自己屏幕具体情况调整为1080p、2k等16:9的比例,同时运行rename_pose.sh
```
python start.py -S 1LXtFkjw3qL.glb
bash rename_pose.bash
```
:warning: 记得在每次准备收集一条新轨迹时都一定要运行rename_pose.bash！
飞到预定的起飞地点后，运行get_traj.sh，然后切回Viewer窗口开始正常操控即可
```
bash get_traj.bash
```

飞到预定终点降落后，按一下esc即可退出模拟器

## 3.3 轨迹处理
收集完轨迹时，坐标文件会保存在当前目录的saved_transformations中，需要使用removal.py删除冗余帧
```
python removal.py -P saved_transformations/
```
然后在场景文件夹下新建traj_1、traj_2等格式的文件并将saved_transformations剪切过去
```
mkdir  1LXtFkjw3qL/traj_1
mv saved_transformations/ 1LXtFkjw3qL/traj_1/
```
之后即可开始在该场景下采集下一条轨迹，回到3.2的流程

在采集完当前场景下的轨迹后，使用inverse.py对轨迹进行增广
```
python inverse.py -P 1LXtFkjw3qL
```
该脚本会将采集到的轨迹的起点和终点互换得到一条新的轨迹

最后将收集好的场景和轨迹文件分别移至相应的文件(scene/和UNDONE/)即可

## 3.4 图像收集
使用get_screen.py批量自动收集图像
```
python get_screen.py
```
:warning: 注意使用前请修改脚本中的全局变量 PATH_TO_GLB和SLEEPTIME，前者是轨迹文件和场景文件的路径映射，后者是每次打开对应场景预计的时间，可以使用habitat-viewer打开场景同时用手机秒表记一下时，这个时间是影响收集速度的最关键因素，所以应该尽量接近场景打开的时间，如果没有设置则默认为休眠3s，在收集大量图像时会十分影响效率。整个过程会十分耗时，HM3D中场景打开时间在1.2s-2.6s左右，加上其他的一些处理时间，采集一张图片大概平均2.4s，收集1.8w张图片则需要12h，同时在收集过程中不能使用电脑，尤其不能使用键盘，所以请注意好时间分配，尽量在睡觉已经确定不使用电脑的时候收集。:warning:

收集完图像之后，删除已使用的场景glb文件，并将轨迹文件移至DONE即可

# 4. 其他注意事项
- 飞行轨迹中，在穿门、上下楼梯以及狭长过道中时需要操作细致，可以一下一下点按，尽量做到看上去没有碰撞
- 选取起点时，可以同时也注意一下背后180°的环境，能有什么参照物更好，因为翻转增广之后就成了新轨迹的终点
- 打开新场景时，可以飞出场景外看看场景结构、复杂度，有多少层，多少房间之类的，之后收集的轨迹最好覆盖大部分的房间、厅室
- 在降落时如果多按了一下降落导致飞到地下去了，可以在removal.py之后使用
  ```
  habitat-viewer xxx.glb --agent-transform-filepath saved_transformations/最后几帧.txt
  ```
  打开场景后按一下]键，即可加载到对应位置查看该帧是不是掉地下去了，然后删除掉下去的帧即可，不用全部重飞
- 使用get_screenshots.py获取完图像后，可以看一下每个traj文件夹下的saved_transformations和screenshots文件数是否相同，然后每个场景随便选一个traj看看图像是否正常即可
- 如果get_screenshots.py收集到的某条轨迹图像有问题需重新采集，只需删除这一条轨迹的screenshots然后重新运行即可，该采集脚本会自动略过已经存在screenshots文件夹的轨迹
- 在飞行轨迹时尽量一次只执行一种动作，避免在直行的同时这种复合动作的出现以方便后续动作标注
