# unet_exp
hl进展

# 数据集
- msd 10个task
链接: https://pan.baidu.com/s/13QyioAcNbHCk7QpRJ0B4pA 提取码: a9g2
--来自百度网盘超级会员v6的分享

- msd nnunet 预处理
链接: https://pan.baidu.com/s/1RnE3LOQE6y3COdLL6tlMdA 提取码: ugu0
--来自百度网盘超级会员v6的分享

- CT spine 1k

# 环境
```shell
# 装torch
conda create -n torch python=3.9
conda activate torch
conda update -n base -c defaults conda
nvcc --version
conda install pytorch torchvision torchaudio cpuonly -c pytorch

# 装nnunet
pip install -r requirements.txt
git clone https://github.com/MIC-DKFZ/nnUNet.git
cd nnUNet
pip install -e .
pip install --upgrade git+https://ghproxy.com/https://github.com/FabianIsensee/hiddenlayer.git@more_plotted_details#egg=hiddenlayer
pip install matplotlib
```

# 设置环境变量
```shell
data_dir=/home/lin/Desktop/data/nnunet
# data_dir=/home/work/prep
export nnUNet_raw_data_base=${data_dir}
export nnUNet_preprocessed=${data_dir}/nnUNet_preprocessed
export RESULTS_FOLDER=${data_dir}/RESULTS_FOLDER

echo  nnUNet_raw_data_base: ${nnUNet_raw_data_base}
echo  nnUNet_preprocessed: ${nnUNet_preprocessed}
echo  RESULTS_FOLDER: ${RESULTS_FOLDER}

```

# nnunet预处理

nnUNet_convert_decathlon_task -i /home/lin/Desktop/msd # 4d序列会拆分成3d

nnUNet_plan_and_preprocess -t 6 -tl 1 -tf 1 --verify_dataset_integrity

预处理流程
1. 裁剪数据，找到扫描中非0的部分，用bb包起来，把bb里的裁出来。对头部这种目标小的会有用。每个扫描在 nnUNet_cropped_data 下一个 npz，一个pkl。
2. 计算每组扫描和整个数据集的统计信息：median，mean，sd，mn，mx，percentile_99_5，percentile_00_5。写data_properties.pkl和intensityproperties.pkl
3. 生成计划，都是规则，很快也就1s
4. 进行预处理，每次都是从头开始没有断点
